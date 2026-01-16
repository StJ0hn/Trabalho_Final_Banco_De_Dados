-- 1. Tabela de Auditoria (Necessária para o log)
CREATE TABLE IF NOT EXISTS log_auditoria (
    id_log SERIAL PRIMARY KEY,
    tabela_afetada VARCHAR(50),
    acao VARCHAR(50),
    usuario VARCHAR(50),
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    detalhe TEXT
);

-- TRIGGER 1: Log de Exclusão de Cliente
CREATE OR REPLACE FUNCTION func_log_delete_cliente() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO log_auditoria (tabela_afetada, acao, usuario, detalhe)
    VALUES ('cliente', 'DELETE', current_user, 'Cliente ID ' || OLD.id_cliente || ' removido.');
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_audit_delete_cliente
AFTER DELETE ON cliente
FOR EACH ROW EXECUTE FUNCTION func_log_delete_cliente();

-- TRIGGER 2: Atualização Automática de Saldo do Proprietário
-- Regra: Quando um pagamento entra, o saldo do dono aumenta.
CREATE OR REPLACE FUNCTION func_atualiza_saldo_dono() RETURNS TRIGGER AS $$
BEGIN
    UPDATE proprietario
    SET saldo = saldo + NEW.valor
    WHERE cpf = (SELECT cpf FROM proprietario LIMIT 1);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_pagamento_realizado
AFTER INSERT ON pagamento
FOR EACH ROW EXECUTE FUNCTION func_atualiza_saldo_dono();

-- TRIGGER 3: Previne remoção de Plano em uso (Integridade)
CREATE OR REPLACE FUNCTION func_protege_plano() RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM cliente WHERE id_plano_atual = OLD.id_plano) THEN
        RAISE EXCEPTION 'Não é possível remover este plano pois há clientes vinculados.';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_protege_plano
BEFORE DELETE ON plano
FOR EACH ROW EXECUTE FUNCTION func_protege_plano();