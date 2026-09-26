

-- ==========================================
-- 1. Create the Database
-- ==========================================
CREATE DATABASE WindowsLogIntelligence;
GO

USE WindowsLogIntelligence;
GO

-- ==========================================
-- 2. Core Table: Raw Windows Events
-- ==========================================
-- This stores the raw data extracted from Windows Event Viewer.
CREATE TABLE WindowsEventLogs (
    LogID             INT IDENTITY(1,1) PRIMARY KEY, -- Surrogate key for fast indexing
    EventID           INT NOT NULL,                  -- e.g., 4624, 4625, 7031
    LogName           VARCHAR(50) NOT NULL,          -- 'Security', 'System', 'Application'
    SourceName        VARCHAR(255) NOT NULL,         -- e.g., 'Microsoft-Windows-Security-Auditing'
    ComputerName      VARCHAR(255) NOT NULL,         -- The machine that generated the log
    TimeGenerated     DATETIME2 NOT NULL,            -- When the event actually happened
    TimeWritten       DATETIME2 NOT NULL,            -- When it was written to the DB
    EventType         INT NOT NULL,                  -- 0=Info, 1=Error, 2=Warning, etc.
    EventLevel        VARCHAR(20) NOT NULL,          -- 'Information', 'Warning', 'Error', 'Critical'
    UserSID           VARCHAR(255) NULL,             -- Security Identifier (Crucial for Security logs)
    UserName          VARCHAR(255) NULL,             -- Resolved username (if available)
    EventData         NVARCHAR(MAX) NULL             -- Raw XML payload of the event
);
GO

-- Indexes for fast querying (Crucial for ML and Dashboards)
CREATE INDEX IX_EventLogs_TimeGenerated ON WindowsEventLogs(TimeGenerated);
CREATE INDEX IX_EventLogs_EventID ON WindowsEventLogs(EventID);
CREATE INDEX IX_EventLogs_LogName ON WindowsEventLogs(LogName);
GO

-- ==========================================
-- 3. Reference Table: Event Definitions
-- ==========================================
-- This acts as a dictionary. It helps your ML model and dashboard 
-- understand what an Event ID actually means without hardcoding it in Python.
CREATE TABLE EventDefinitions (
    EventID           INT PRIMARY KEY,
    EventName         VARCHAR(255) NOT NULL,         -- e.g., 'Failed Logon', 'Service Crash'
    Category          VARCHAR(100) NOT NULL,         -- e.g., 'Logon/Logoff', 'System Failure'
    Severity          VARCHAR(20) NOT NULL,          -- 'Low', 'Medium', 'High', 'Critical'
    IsSecurityEvent   BIT NOT NULL DEFAULT 0         -- 1 = Security relevant, 0 = Normal
);
GO

-- Pre-populate with common Security Log Event IDs to get you started
INSERT INTO EventDefinitions (EventID, EventName, Category, Severity, IsSecurityEvent) VALUES
(4624, 'Successful Logon', 'Logon/Logoff', 'Low', 1),
(4625, 'Failed Logon', 'Logon/Logoff', 'Medium', 1),
(4634, 'Logoff', 'Logon/Logoff', 'Low', 1),
(4648, 'Explicit Credential Logon', 'Logon/Logoff', 'Medium', 1),
(4720, 'User Account Created', 'Account Management', 'Medium', 1),
(4722, 'User Account Enabled', 'Account Management', 'Medium', 1),
(4724, 'Password Reset Attempt', 'Account Management', 'High', 1),
(4740, 'Account Locked Out', 'Account Management', 'High', 1),
(1102, 'Audit Log Cleared', 'System Security', 'Critical', 1),
(7031, 'Service Terminated Unexpectedly', 'System Failure', 'High', 0),
(1000, 'Application Error', 'Application Failure', 'Medium', 0);
GO

-- ==========================================
-- 4. Output Table: ML Predictions
-- ==========================================
-- This stores the results of your Logistic Regression / Anomaly Detection models.
-- Your Streamlit dashboard will query this table to show alerts.
CREATE TABLE MLPredictions (
    PredictionID      INT IDENTITY(1,1) PRIMARY KEY,
    LogID             INT NOT NULL,                  -- Links back to the specific event
    ModelName         VARCHAR(100) NOT NULL,         -- e.g., 'LogReg_Security_v1'
    PredictionLabel   VARCHAR(100) NOT NULL,         -- e.g., 'Normal', 'Anomaly', 'Brute Force'
    ConfidenceScore   FLOAT NOT NULL,                -- Probability (0.0 to 1.0) or anomaly score
    PredictedAt       DATETIME2 DEFAULT SYSDATETIME()-- When the model made the prediction
    
    CONSTRAINT FK_MLPredictions_Logs FOREIGN KEY (LogID) REFERENCES WindowsEventLogs(LogID)
);
GO

CREATE INDEX IX_MLPredictions_LogID ON MLPredictions(LogID);
CREATE INDEX IX_MLPredictions_Label ON MLPredictions(PredictionLabel);
GO