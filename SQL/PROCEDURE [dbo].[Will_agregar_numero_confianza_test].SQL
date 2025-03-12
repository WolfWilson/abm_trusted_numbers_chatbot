USE [Gestion]
GO
/****** Object:  StoredProcedure [dbo].[Will_agregar_numero_confianza_test]    Script Date: 12/03/2025 09:36:03 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[Will_agregar_numero_confianza_test]
    @Cuil BIGINT,          -- CUIL del beneficiario
    @Pais VARCHAR(5),      -- Código de país
    @Area VARCHAR(5),      -- Código de área
    @Abonado VARCHAR(15),  -- Número de abonado
    @Referencia VARCHAR(50), -- Descripción o referencia
    @Principal BIT,        -- Si es principal (1=Sí, 0=No)
    @Notificacion BIT      -- Si recibe notificaciones (1=Sí, 0=No)
AS
BEGIN
    SET NOCOUNT ON;

    -- Verifica si el CUIL ya tiene el mismo número registrado
    IF EXISTS (SELECT 1 FROM Principal.Credenciales.dbo.celular_confianza WHERE cuil = @Cuil AND pais = @Pais AND area = @Area AND abonado = @Abonado)
    BEGIN
        PRINT 'El número ya está registrado para este CUIL.';
        RETURN;
    END

    -- Insertar el nuevo número sin necesidad de incluir `telchatbot` (se genera automáticamente)
    INSERT INTO Credenciales.dbo.celular_confianza (
        cuil, pais, area, abonado, referencia, principal, notificacion
    ) VALUES (
        @Cuil, @Pais, @Area, @Abonado, @Referencia, @Principal, @Notificacion
    );

    PRINT 'Número agregado correctamente.';
END;

/*
Ejemplo de ejecución:
EXEC Will_agregar_numero_confianza_test 
    @Cuil = 20078348292,
    @Pais = '54',
    @Area = '11',
    @Abonado = '12345678',
    @Referencia = 'Número personal',
    @Principal = 1,
    @Notificacion = 1;
*/
