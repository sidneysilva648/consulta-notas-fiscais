import os

def conectar_salesforce():
    try:
        from simple_salesforce import Salesforce
        sf = Salesforce(
            username=os.environ.get("SF_USERNAME"),
            password=os.environ.get("SF_PASSWORD"),
            security_token=os.environ.get("SF_SECURITY_TOKEN", ""),
            domain=os.environ.get("SF_DOMAIN", "login")
        )
        return sf
    except Exception as e:
        raise Exception(f"Erro ao conectar: {str(e)}")

def buscar_nota_fiscal(numero_nf: str, serie: str = ""):
    try:
        sf = conectar_salesforce()

        # Filtro por número da NF e série
        where = f"Name = '{numero_nf}'"
        if serie:
            where += f" AND Serie__c = '{serie}'"

        query = f"""
            SELECT 
                Id,
                Name,
                Serie__c,
                Referencia__c,
                Telefone__c,
                Status__c,
                Data_do_Documento__c,
                Conta__c
            FROM Invoice__c
            WHERE {where}
            LIMIT 1
        """

        resultado = sf.query(query)
        registros = resultado.get("records", [])

        if not registros:
            return None, "Nota fiscal não encontrada."

        dados = registros[0]
        return {
            "numero_nf": dados.get("Name", numero_nf),
            "serie": dados.get("Serie__c", "Não informado"),
            "telefone": dados.get("Telefone__c", "Não informado"),
            "ponto_referencia": dados.get("Referencia__c", "Não informado"),
            "status": dados.get("Status__c", "Não informado"),
            "data": dados.get("Data_do_Documento__c", "Não informado"),
        }, None

    except Exception as e:
        return None, f"Erro: {str(e)}"
