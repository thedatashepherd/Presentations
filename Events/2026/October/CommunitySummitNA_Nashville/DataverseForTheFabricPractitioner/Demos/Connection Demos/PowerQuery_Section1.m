section Section1;

shared account = let
    Source = CommonDataService.Database(pDataverseHost, [CreateNavigationProperties = false]),
    dbo_account = Source{[Schema="dbo",Item="account"]}[Data]
in
    dbo_account;

shared DataverseTableMetadata = let
    Source = Json.Document(Web.Contents("https://" & pDataverseApiHost & "/api/data/v9.2/EntityDefinitions?$select=LogicalName,SchemaName,EntitySetName,ObjectTypeCode,IsCustomEntity,IsManaged,DisplayName,ChangeTrackingEnabled,PrimaryIdAttribute,PrimaryNameAttribute")),
    value = Source[value],
    ToTable = Table.FromList(value, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    Expanded = Table.ExpandRecordColumn(ToTable, "Column1", {"LogicalName","SchemaName","EntitySetName","ObjectTypeCode","IsCustomEntity","IsManaged","DisplayName", "ChangeTrackingEnabled","PrimaryIdAttribute","PrimaryNameAttribute"}),
    AddLabel = Table.AddColumn(Expanded, "DisplayLabel", each try [DisplayName][UserLocalizedLabel][Label] otherwise null),
    Final = Table.SelectColumns(Table.RemoveColumns(AddLabel, {"DisplayName"}), {"LogicalName","SchemaName","EntitySetName","ObjectTypeCode","IsCustomEntity","IsManaged","ChangeTrackingEnabled","DisplayLabel","PrimaryIdAttribute","PrimaryNameAttribute"})
in
    Final;

shared DataverseColumnMetadata = let
    TableNames = List.Buffer(List.Distinct(List.RemoveNulls(DataverseTableMetadata[LogicalName]))),
    GetAttrs = (tbl as text) as table =>
        let
            BaseUrl = "https://" & pDataverseApiHost,
            Path = "api/data/v9.2/EntityDefinitions(LogicalName='" & tbl & "')/Attributes",
            Response = Json.Document(Web.Contents(BaseUrl, [RelativePath=Path, Query=[#"$select"="LogicalName,SchemaName,AttributeType,AttributeTypeName,DisplayName,RequiredLevel,IsCustomAttribute,IsPrimaryId,IsPrimaryName"]])),
            Attributes = Table.FromRecords(Response[value], {"LogicalName","SchemaName","AttributeType","AttributeTypeName","DisplayName","RequiredLevel","IsCustomAttribute","IsPrimaryId","IsPrimaryName"}, MissingField.UseNull),
            LookupResponse = Json.Document(Web.Contents(BaseUrl, [RelativePath=Path & "/Microsoft.Dynamics.CRM.LookupAttributeMetadata", Query=[#"$select"="LogicalName,Targets"]])),
            Lookups = Table.FromRecords(LookupResponse[value], {"LogicalName","Targets"}, MissingField.UseNull),
            Targets = Table.AddColumn(Lookups, "LookupTargets", each if [Targets] = null then null else Text.Combine(List.Transform([Targets], each Text.From(_)), ", "), type nullable text),
            Joined = Table.NestedJoin(Attributes, {"LogicalName"}, Targets, {"LogicalName"}, "LookupMetadata", JoinKind.LeftOuter),
            Expanded = Table.ExpandTableColumn(Joined, "LookupMetadata", {"LookupTargets"}, {"LookupTargets"}),
            AddTable = Table.AddColumn(Expanded, "TableLogicalName", each tbl, type text),
            AddType = Table.AddColumn(AddTable, "AttributeTypeText", each try [AttributeTypeName][Value] otherwise null, type nullable text),
            AddLabel = Table.AddColumn(AddType, "ColumnDisplayLabel", each try [DisplayName][UserLocalizedLabel][Label] otherwise null, type nullable text),
            AddRequired = Table.AddColumn(AddLabel, "RequiredLevelText", each try [RequiredLevel][Value] otherwise null, type nullable text),
            Renamed = Table.RenameColumns(AddRequired, {{"LogicalName","ColumnLogicalName"},{"SchemaName","ColumnSchemaName"}}),
            Result = Table.SelectColumns(Renamed, {"TableLogicalName","ColumnLogicalName","ColumnSchemaName","ColumnDisplayLabel","AttributeType","AttributeTypeText","RequiredLevelText","IsCustomAttribute","IsPrimaryId","IsPrimaryName","LookupTargets"})
        in
            Result,
    Output = if List.IsEmpty(TableNames) then #table({"TableLogicalName","ColumnLogicalName","ColumnSchemaName","ColumnDisplayLabel","AttributeType","AttributeTypeText","RequiredLevelText","IsCustomAttribute","IsPrimaryId","IsPrimaryName","LookupTargets"}, {}) else Table.Combine(List.Transform(TableNames, each GetAttrs(_)))
in
    Output;


shared Selected_Table_Columns = let
    TableNames = List.Distinct(List.Select(List.Transform(Text.Split(pMetadataTables, ","), each Text.Lower(Text.Trim(_))), each _ <> "")),
    GetAttrs = (tbl as text) as table =>
        let
            BaseUrl = "https://" & pDataverseApiHost,
            Path = "api/data/v9.2/EntityDefinitions(LogicalName='" & tbl & "')/Attributes",
            Response = Json.Document(Web.Contents(BaseUrl, [RelativePath=Path, Query=[#"$select"="LogicalName,SchemaName,AttributeType,AttributeTypeName,DisplayName,RequiredLevel,IsCustomAttribute,IsPrimaryId,IsPrimaryName"]])),
            Attributes = Table.FromRecords(Response[value], {"LogicalName","SchemaName","AttributeType","AttributeTypeName","DisplayName","RequiredLevel","IsCustomAttribute","IsPrimaryId","IsPrimaryName"}, MissingField.UseNull),
            LookupResponse = Json.Document(Web.Contents(BaseUrl, [RelativePath=Path & "/Microsoft.Dynamics.CRM.LookupAttributeMetadata", Query=[#"$select"="LogicalName,Targets"]])),
            Lookups = Table.FromRecords(LookupResponse[value], {"LogicalName","Targets"}, MissingField.UseNull),
            Targets = Table.AddColumn(Lookups, "LookupTargets", each if [Targets] = null then null else Text.Combine(List.Transform([Targets], each Text.From(_)), ", "), type nullable text),
            Joined = Table.NestedJoin(Attributes, {"LogicalName"}, Targets, {"LogicalName"}, "LookupMetadata", JoinKind.LeftOuter),
            Expanded = Table.ExpandTableColumn(Joined, "LookupMetadata", {"LookupTargets"}, {"LookupTargets"}),
            AddTable = Table.AddColumn(Expanded, "TableLogicalName", each tbl, type text),
            AddType = Table.AddColumn(AddTable, "AttributeTypeText", each try [AttributeTypeName][Value] otherwise null, type nullable text),
            AddLabel = Table.AddColumn(AddType, "ColumnDisplayLabel", each try [DisplayName][UserLocalizedLabel][Label] otherwise null, type nullable text),
            AddRequired = Table.AddColumn(AddLabel, "RequiredLevelText", each try [RequiredLevel][Value] otherwise null, type nullable text),
            Renamed = Table.RenameColumns(AddRequired, {{"LogicalName","ColumnLogicalName"},{"SchemaName","ColumnSchemaName"}}),
            Result = Table.SelectColumns(Renamed, {"TableLogicalName","ColumnLogicalName","ColumnSchemaName","ColumnDisplayLabel","AttributeType","AttributeTypeText","RequiredLevelText","IsCustomAttribute","IsPrimaryId","IsPrimaryName","LookupTargets"})
        in
            Result,
    Output = if List.IsEmpty(TableNames) then #table({"TableLogicalName","ColumnLogicalName","ColumnSchemaName","ColumnDisplayLabel","AttributeType","AttributeTypeText","RequiredLevelText","IsCustomAttribute","IsPrimaryId","IsPrimaryName","LookupTargets"}, {}) else Table.Combine(List.Transform(TableNames, each GetAttrs(_)))
in
    Output;


shared Dataverse_SQL_Columns = let
    Source = Sql.Database(pDataverseHost, pDataverseDatabaseName, [Query="SELECT#(lf)    t.name AS table_name,#(lf)    c.name AS column_name,#(lf)    ty.name AS data_type,#(lf)    CASE#(lf)        WHEN ty.name IN ('nvarchar', 'nchar')#(lf)            THEN CASE#(lf)                    WHEN c.max_length = -1 THEN -1#(lf)                    ELSE c.max_length / 2#(lf)                 END#(lf)        WHEN ty.name IN ('varchar', 'char', 'varbinary', 'binary')#(lf)            THEN c.max_length#(lf)        ELSE NULL#(lf)    END AS character_maximum_length,#(lf)    CASE#(lf)        WHEN ty.name IN ('varchar', 'char', 'varbinary', 'binary')#(lf)        THEN#(lf)            ty.name + '('#(lf)            + CASE#(lf)                WHEN c.max_length = -1 THEN 'MAX'#(lf)                ELSE CAST(c.max_length AS varchar(10))#(lf)              END#(lf)            + ')'#(lf)        WHEN ty.name IN ('nvarchar', 'nchar')#(lf)        THEN#(lf)            ty.name + '('#(lf)            + CASE#(lf)                WHEN c.max_length = -1 THEN 'MAX'#(lf)                ELSE CAST(c.max_length / 2 AS varchar(10))#(lf)              END#(lf)            + ')'#(lf)        WHEN ty.name IN ('decimal', 'numeric')#(lf)        THEN#(lf)            ty.name + '('#(lf)            + CAST(c.precision AS varchar(10))#(lf)            + ','#(lf)            + CAST(c.scale AS varchar(10))#(lf)            + ')'#(lf)        ELSE ty.name#(lf)    END AS human_readable_data_type,#(lf)    c.is_nullable,#(lf)    c.column_id#(lf)FROM sys.columns AS c#(lf)LEFT JOIN sys.tables AS t#(lf)    ON c.object_id = t.object_id#(lf)LEFT JOIN sys.types AS ty#(lf)    ON c.user_type_id = ty.user_type_id#(lf)ORDER BY#(lf)    t.name,#(lf)    c.column_id;", CreateNavigationProperties=false])
in
    Source;

shared Account_SQL_Columns = let
    Source = Sql.Database(pDataverseHost, pDataverseDatabaseName, [Query="SELECT c.*, #(lf)    t.name AS table_name,#(lf)    c.name AS column_name,#(lf)    ty.name AS data_type,#(lf)    CASE#(lf)        WHEN ty.name IN ('nvarchar', 'nchar')#(lf)            THEN CASE#(lf)                    WHEN c.max_length = -1 THEN -1#(lf)                    ELSE c.max_length / 2#(lf)                 END#(lf)        WHEN ty.name IN ('varchar', 'char', 'varbinary', 'binary')#(lf)            THEN c.max_length#(lf)        ELSE NULL#(lf)    END AS character_maximum_length,#(lf)    CASE#(lf)        WHEN ty.name IN ('varchar', 'char', 'varbinary', 'binary')#(lf)        THEN#(lf)            ty.name + '('#(lf)            + CASE#(lf)                WHEN c.max_length = -1 THEN 'MAX'#(lf)                ELSE CAST(c.max_length AS varchar(10))#(lf)              END#(lf)            + ')'#(lf)        WHEN ty.name IN ('nvarchar', 'nchar')#(lf)        THEN#(lf)            ty.name + '('#(lf)            + CASE#(lf)                WHEN c.max_length = -1 THEN 'MAX'#(lf)                ELSE CAST(c.max_length / 2 AS varchar(10))#(lf)              END#(lf)            + ')'#(lf)        WHEN ty.name IN ('decimal', 'numeric')#(lf)        THEN#(lf)            ty.name + '('#(lf)            + CAST(c.precision AS varchar(10))#(lf)            + ','#(lf)            + CAST(c.scale AS varchar(10))#(lf)            + ')'#(lf)        ELSE ty.name#(lf)    END AS human_readable_data_type,#(lf)    c.is_nullable,#(lf)    c.column_id#(lf)FROM sys.columns AS c#(lf)LEFT JOIN sys.tables AS t#(lf)    ON c.object_id = t.object_id#(lf)LEFT JOIN sys.types AS ty#(lf)    ON c.user_type_id = ty.user_type_id#(lf)WHERE t.name = 'account'", CreateNavigationProperties=false])
in
    Source;

shared pDataverseHost = "YOURORG.crm.dynamics.com" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true];

shared pDataverseApiHost = "YOURORG.api.crm.dynamics.com" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true];

shared pDataverseDatabaseName = "YOUR_DATAVERSE_DATABASE_NAME" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true];

shared Dataverse_Generated_Connection = let
    Source = CommonDataService.Database(pDataverseHost, [CreateNavigationProperties = false]),
    dbo_account = Source{[Schema="dbo",Item="account"]}[Data]
in
    dbo_account;

shared FetchXML_AccountSample = let
    RowLimit = if pFetchXMLRowLimit > 0 and Number.RoundDown(pFetchXMLRowLimit) = pFetchXMLRowLimit then pFetchXMLRowLimit else error "pFetchXMLRowLimit must be a positive whole number.",
    FetchXml =
        "<fetch top='" & Text.From(RowLimit, "en-US") & "'>" &
        "  <entity name='account'>" &
        "    <attribute name='accountid' />" &
        "    <attribute name='name' />" &
        "    <attribute name='createdon' />" &
        "    <order attribute='name' />" &
        "  </entity>" &
        "</fetch>",

    Response = Json.Document(
        Web.Contents(
            "https://" & pDataverseApiHost,
            [
                RelativePath = "api/data/v9.2/accounts",
                Query = [fetchXml = FetchXml],
                Headers = [Accept = "application/json"]
            ]
        )
    ),

    Result = Table.FromRecords(
        Response[value],
        {"accountid", "name", "createdon"},
        MissingField.UseNull
    )
in
    Result;
shared pMetadataTables = "account,contact" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true];
shared pFetchXMLRowLimit = 10 meta [IsParameterQuery=true, Type="Number", IsParameterQueryRequired=true];
