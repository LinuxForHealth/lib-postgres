CREATE OR REPLACE PROCEDURE test_db_schema_name.sp_patient_batch_status_update (patbatchid BIGINT, patbatchstatus smallint)
LANGUAGE plpgsql
AS $$
DECLARE
    hl7batchid BIGINT;
BEGIN
        UPDATE test_db_schema_name.patientfhirbatch pfb
            SET patbatch_status = patbatchstatus
            WHERE patbatch_id = patbatchid
            RETURNING pfb.hl7batch_id INTO hl7batchid;
        IF (SELECT COUNT(pfb.patbatch_id) FROM test_db_schema_name.patientfhirbatch pfb WHERE hl7batch_id=hl7batchid and patbatch_status < 4) = 0
        THEN
            DELETE FROM test_db_schema_name.hl7batch hl7b
                WHERE hl7b.hl7batch_id=hl7batchid;
        END IF;
END $$