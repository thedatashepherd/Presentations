SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [Data].[Product](
	[ProductKey] [int] NOT NULL,
	[Product Code] [nvarchar](255) NULL,
	[Product Name] [nvarchar](500) NULL,
	[Manufacturer] [nvarchar](50) NULL,
	[Brand] [nvarchar](50) NULL,
	[Color] [nvarchar](20) NOT NULL,
	[Weight Unit Measure] [nvarchar](20) NULL,
	[Weight] [float] NULL,
	[Unit Cost] [money] NULL,
	[Unit Price] [money] NULL,
	[Subcategory Code] [nvarchar](100) NULL,
	[Subcategory] [nvarchar](50) NULL,
	[Category Code] [nvarchar](100) NULL,
	[Category] [nvarchar](30) NULL
) ON [PRIMARY]
GO
ALTER TABLE [Data].[Product] ADD PRIMARY KEY CLUSTERED 
(
	[ProductKey] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
