USE [Gestion]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[Will_obtener_datos_chatbot_cred_test]
    @Nro_doc INT  
AS
BEGIN
    SET NOCOUNT ON;

    ------------------------------------------------
    -- 1) Crear tabla intermedia @JubiData
    ------------------------------------------------
    DECLARE @JubiData TABLE (
        CUIL BIGINT PRIMARY KEY,
        Nombre NVARCHAR(255),
        Nro_jub INT,
        Nro_doc INT,
        Activo INT,
        Tipo_Benef NVARCHAR(MAX)
    );

    ------------------------------------------------
    -- 2) Insertar registros de Jubi
    ------------------------------------------------
    INSERT INTO @JubiData (CUIL, Nombre, Nro_jub, Nro_doc, Activo, Tipo_Benef)
    SELECT 
        J.CUIL,
        MAX(J.Nombre)  AS Nombre,  
        MAX(J.Nro_jub) AS Nro_jub,
        J.Nro_doc,
        MAX(J.Activo)  AS Activo,
        '' AS Tipo_Benef
    FROM DSP.dbo.Jubi AS J
    WHERE J.Nro_doc = @Nro_doc
      AND J.Activo = 0
    GROUP BY J.CUIL, J.Nro_doc;

    ------------------------------------------------
    -- 3) Actualizar Tipo_Benef concatenado (si hubiera varios)
    ------------------------------------------------
    UPDATE JD
    SET Tipo_Benef = STUFF((
        SELECT DISTINCT ' / ' +
            CASE J2.Tipo_Benef 
                WHEN 0 THEN 'Haberes Impagos'
                WHEN 1 THEN 'Pensión'
                WHEN 2 THEN 'Jubilación'
                WHEN 3 THEN 'Ley 5496'
                WHEN 4 THEN 'Ley 5495'
                WHEN 5 THEN 'Ex Combatiente de Malvinas'
                WHEN 6 THEN 'Movilizados de Malvinas'
                ELSE 'Desconocido'
            END
        FROM DSP.dbo.Jubi AS J2
        WHERE J2.CUIL = JD.CUIL
          AND J2.Activo = 0
        FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 3, ''
    )
    FROM @JubiData JD;

    ------------------------------------------------
    -- 4) Mostrar resultados, incluyendo CUIL
    ------------------------------------------------
    SELECT 
		 D.idcelular,     -- 👈 Lo necesito para obtener el id para eliminar y editar igual estará oculto.
        JD.CUIL,       -- 🔹 CUIL que voy a ocultar
        JD.Nombre,
        JD.Nro_jub,
        JD.Nro_doc,
        JD.Activo,
        JD.Tipo_Benef,
        COALESCE(D.referencia, '') AS referencia,
        COALESCE(
            CAST(D.pais AS VARCHAR) + ' ' + 
            CAST(D.area AS VARCHAR) + ' ' + 
            CAST(D.abonado AS VARCHAR),
            ''
        ) AS telefono,
        COALESCE(D.principal, 0) AS principal, 
        COALESCE(D.notificacion, 0) AS notificacion
    FROM @JubiData AS JD
    LEFT JOIN Credenciales.dbo.celular_confianza AS D
        ON JD.CUIL = D.cuil;
END;
GO

/*
EXEC Will_obtener_datos_chatbot_cred_test @Nro_doc = 21346971;
*/
