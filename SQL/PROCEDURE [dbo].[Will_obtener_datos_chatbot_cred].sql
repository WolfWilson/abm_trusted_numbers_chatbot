USE [Gestion]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[Will_obtener_datos_chatbot_cred]
    @Nro_doc INT  -- Parámetro de entrada (DNI, máximo 8 dígitos)
AS
BEGIN
    SET NOCOUNT ON;

    -- -----------------------------------------------
    -- 1) Tomar datos de Jubi con Activo = 0
    --    desde el servidor SQL01, base DSP.
    -- -----------------------------------------------
    WITH JubiData AS (
        SELECT 
            J.Nombre,      -- Primer campo: Nombre
            J.Nro_jub,
            -- CUIL se sigue usando para hacer el JOIN,
            -- pero ya no se muestra en el SELECT final
            J.CUIL,
            J.Nro_doc,
            J.Activo,
            J.Tipo_Benef
        FROM SQL01.DSP.dbo.Jubi AS J
        WHERE J.Nro_doc = @Nro_doc
          AND J.Activo = 0
    )

    -- -----------------------------------------------
    -- 2) SELECT con LEFT JOIN a celular_confianza
    --    para obtener referencia, teléfono, etc.
    -- -----------------------------------------------
    SELECT 
        -- Nombre, jubilación, etc. se mantienen
        J.Nombre,       
        J.Nro_jub,
        J.Nro_doc,
        J.Activo,
        J.Tipo_Benef,

        -- Se muestra "referencia" en lugar de CUIL
        COALESCE(D.referencia, '') AS referencia,

        -- Teléfono dinámico
        COALESCE(
            CAST(D.pais AS VARCHAR) + ' ' + 
            CAST(D.area AS VARCHAR) + ' ' + 
            CAST(D.abonado AS VARCHAR),
            ''
        ) AS telefono,

        COALESCE(D.principal, 0) AS principal, 
        COALESCE(D.notificacion, 0) AS notificacion
    FROM JubiData AS J
    LEFT JOIN Principal.Credenciales.dbo.celular_confianza AS D
        ON J.CUIL COLLATE SQL_Latin1_General_CP1_CI_AS = 
           D.cuil COLLATE SQL_Latin1_General_CP1_CI_AS

    UNION

    -- -----------------------------------------------
    -- 3) Si no hay coincidencias en celular_confianza,
    --    se muestra Jubi sin teléfono ni referencia
    -- -----------------------------------------------
    SELECT 
        J.Nombre,
        J.Nro_jub,
        J.Nro_doc,
        J.Activo,
        J.Tipo_Benef,
        '' AS referencia,
        '' AS telefono,
        0 AS principal, 
        0 AS notificacion
    FROM JubiData AS J
    WHERE NOT EXISTS (
        SELECT 1 
          FROM Principal.Credenciales.dbo.celular_confianza AS D
         WHERE J.CUIL COLLATE SQL_Latin1_General_CP1_CI_AS = 
               D.cuil COLLATE SQL_Latin1_General_CP1_CI_AS
    );

END;
GO



/*
EXEC Will_obtener_datos_chatbot_cred @Nro_doc = 21346971

*/