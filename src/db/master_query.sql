-- ==========================================
-- 1. CREATE DATABASE (If it doesn't exist)
-- ==========================================
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'WindowsLogIntelligence')
BEGIN
    CREATE DATABASE WindowsLogIntelligence;
    PRINT 'Database WindowsLogIntelligence created.';
END
ELSE
BEGIN
    PRINT 'Database WindowsLogIntelligence already exists.';
END
GO

USE WindowsLogIntelligence;
GO

-- ==========================================
-- 2. CREATE TABLE (If it doesn't exist)
-- ==========================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='EventLog' and xtype='U')
BEGIN
    CREATE TABLE dbo.EventLog (
        Id            INT IDENTITY(1,1) PRIMARY KEY,
        EventID       INT NOT NULL,
        SourceName    NVARCHAR(255) NOT NULL,
        EventType     INT NOT NULL,
        TimeGenerated DATETIME2 NOT NULL,
        ComputerName  NVARCHAR(255) NOT NULL,
        UserName      NVARCHAR(255),
        Message       NVARCHAR(MAX)
    );
    PRINT 'Table dbo.EventLog created.';
END
ELSE
BEGIN
    PRINT 'Table dbo.EventLog already exists.';
END
GO

-- ==========================================
-- 3. CREATE INDEXES (For fast querying)
-- ==========================================
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_EventLog_TimeGenerated')
BEGIN
    CREATE NONCLUSTERED INDEX IX_EventLog_TimeGenerated
    ON dbo.EventLog (TimeGenerated DESC);
END

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_EventLog_EventType')
BEGIN
    CREATE NONCLUSTERED INDEX IX_EventLog_EventType
    ON dbo.EventLog (EventType);
END

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_EventLog_SourceName')
BEGIN
    CREATE NONCLUSTERED INDEX IX_EventLog_SourceName
    ON dbo.EventLog (SourceName);
END

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_EventLog_ComputerName')
BEGIN
    CREATE NONCLUSTERED INDEX IX_EventLog_ComputerName
    ON dbo.EventLog (ComputerName);
END
GO

PRINT 'Setup complete!';