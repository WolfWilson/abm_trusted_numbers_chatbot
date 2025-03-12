USE [Gestion]
GO
/****** Object:  StoredProcedure [dbo].[Will_eliminar_numero_confianza_test]    Script Date: 12/03/2025 09:38:54 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[Will_eliminar_numero_confianza_test]
    @idcelular INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Verifica si existe el número en la tabla
    IF NOT EXISTS (
        SELECT 1 
        FROM Credenciales.dbo.celular_confianza
        WHERE idcelular = @idcelular
    )
    BEGIN
        PRINT 'El número no existe o ya fue eliminado.';
        RETURN;
    END

    -- Elimina el registro
    DELETE FROM Credenciales.dbo.celular_confianza
    WHERE idcelular = @idcelular;

    PRINT 'Número eliminado correctamente.';
END;
