As classes descritas nos arquivos model são implementadas em Python como `dataclasses` no módulo `minicidade/models.py`, que NÃO pode importar `streamlit`.
- Mapeamento de tipos: inteiro = `int`; número = `float`; String = `str`; boolean = `bool`; "List<X>" = `list[X]`; "NULL" = `None` (tipo `X | None`)
- Atributos marcados como "derivado" são calculados pela simulação e não precisam ser salvos
- Atributos marcados como "propriedade" são métodos/propriedades Python, não campos
- Todo modelo salvo tem `to_dict()` e `from_dict()` (ver `04_estrutura_de_codigo.md`); o salvamento é um arquivo JSON com o campo `version`
- Estes arquivos descrevem a ESTRUTURA dos dados. Fórmulas, regras e números de balanceamento estão em `../02_regras_e_constantes.md`, que prevalece em caso de divergência
- `model_07_ui_state.md` descreve o estado da interface Streamlit (`st.session_state`), que é separado do estado da cidade
