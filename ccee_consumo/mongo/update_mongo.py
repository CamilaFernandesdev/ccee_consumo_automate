# MONGO
import re
import logging
import pandas as pd


from infra_copel import MongoHistoricoOficial

logger = logging.getLogger('teste')
logger.propagate = False


class UpdateMongo:
    """
    Classe que faz o update das informações do Mongo quando a base de dados sofre alterações.

    Parâmetros
    ----------
    df: pandas.DataFrame
        Dataframe com as informações a serem atualizadas no MongoDB.
    collection: str
         Nome da collection do MongoDB onde as informações serão atualizadas.
    dicionario: dict[str: list]
         Dicionário com as possibilidades de alterações no nome das colunas na base de dados.
         A chave representa o nome do campo no MongoDB, e a lista contém as possibilidades de nome
         da coluna no DataFrame.

    Atributos
    ---------
    df: pandas.DataFrame
         Dataframe com as informações a serem atualizadas no MongoDB.
    dicionario: dict[str: list]
         Dicionário com as possibilidades de alterações no nome das colunas na base de dados.
    collection_name: str
         Nome da collection do MongoDB onde as informações serão atualizadas.
    column_names: list
         Lista com os nomes das colunas do DataFrame.
    dict_rename: dict
         Dicionário com os nomes renomeados das colunas do DataFrame para os nomes das colunas no MongoDB.
    list_update_new_data: list
         Lista com os dados a serem atualizados no MongoDB.

     Métodos
     -------
    last_document_information()
         Retorna a última linha da collection do MongoDB em uma Series do pandas.
    _create_dict_rename()
         Cria um dicionário com os nomes renomeados das colunas do DataFrame para os nomes das colunas no MongoDB.
    verification_methods(columns_number=8)
         Verifica se houve alteração na quantidade ou no nome das colunas do DataFrame.
    _rename_column()
         Renomeia as colunas do DataFrame com base no dicionário criado em _create_dict_rename().
    dados_para_upload()
         Retorna uma lista com os dados a serem atualizados no MongoDB.
    update_mongo()
         Atualiza os dados no MongoDB.

    Exemplo
    -------
    >>> df = pd.DataFrame({'coluna1': [1, 2, 3], 'coluna2': [4, 5, 6]})
    >>> dicionario = {'nome_coluna1_no_mongo': ['coluna1', 'Coluna1'], 'nome_coluna2_no_mongo': ['coluna2', 'Coluna2']}
    >>> update_mongo = UpdateMongo(df, 'minha_collection', dicionario)
    >>> update_mongo.verification_methods(columns_number=2)
    Funcionou lindamente!
    >>> update_mongo.update_mongo()"""

    def __init__(self, df: pd.DataFrame, collection: str, dicionario: dict[str:list]):
        """Estrutura - code.py.

        # Key: nomes dos campus do Mongo
        # Value: as possibilidade de alterações no nome das colunas na base de dados
        """
        self.df = df
        self.dicionario = dicionario
        self.collection_name = collection

        # Variáveis que serão preenchidas após executar os métodos
        self.column_names = list(self.df.columns)
        self.dict_rename = dict()
        self.list_update_new_data = list()

        logger.info('Conexão com o MongoDB')
        self.mdb = MongoHistoricoOficial()
        self.collection = self.mdb[self.collection_name]

    def last_document_information(self):
        """
        Retorna a última linha da collection do MongoDB em uma Series do pandas.

        Retorna
        -------
        pandas.Series
            Series com a última linha da collection do MongoDB.
        """
        logger.info("Buscando no mongo o documento com a data mais recente")
        self.last_document = list(
            self.collection.find().sort("dia", -1).limit(1))

        # Informação da últimos dado da collection em series pandas
        self.df_last_document = pd.Series(self.last_document[0])
        self.df_last_document = self.df_last_document.drop(index="_id")

        return self.df_last_document

    def _create_dict_rename(self):
        """Cria um dicionário de renomeação de colunas utilizando expressões regulares.

        A função itera sobre o dicionário `dicionario` passado como parâmetro no construtor da classe.
        Para cada key e value no dicionário, a função itera sobre as expressões regulares na lista de value.
        Com as expressões regulares, a função identifica os nomes de colunas da base de dados que
        correspondem às expressões e os adiciona como keys no dicionário `dict_rename`, com o nome
        correspondente da key do dicionário `dicionario` como value.
        """
        # Como os dados CCEE alteram constantemente
        # Cria um dicionário de renomeação utilizando dict comprehension e regex
        for key, list_value in self.dicionario.items():
            for regex in list_value:
                self.dict_rename.update(
                    {
                        column: key
                        for column in self.column_names
                        if re.match(regex, column)
                    }
                )

    def verification_methods(self, columns_number=8):
        # Verifica a quantidade de colunas devido mudanças na base de dados
        if len(self.column_names) != columns_number:
            raise Exception(
                "A quantidade de colunas da base de dados foi alterada.")
        else:
            self._create_dict_rename()
            # Verifica se todos os nomes foram renomeados corretamente
            if set(self.dict_rename.keys()) == set(self.column_names) and set(
                self.dict_rename.values()
            ) == set(self.dicionario.keys()):
                logger.info(
                    "O método de verificação dos dados realizado, não houve alteração na base de dados")
            else:
                raise Exception(
                    "Houve alteração no nome das colunas da base de dados.")

    def _rename_column(self):
        return self.df.rename(columns=self.dict_rename, inplace=True)

    def dados_para_upload(self) -> list[dict]:
        """
        Método que prepara os dados para upload no MongoDB.

        Returns
        -------
            Uma lista de dicionários contendo as informações que serão atualizadas no MongoDB.
        """
        self._rename_column()
        try:
            # Itera pelas colunas e verifica se os valores são iguais
            for idx, row in self.df.iterrows():
                # Verifica se os valores da linha são iguais aos valores do segundo dataframe
                self.list_update_new_data.append(row.to_dict())
                # Compara os dados e gt retorna os valores como boolean
                # Se diferente retorna True
                result_compare = row.gt(self.df_last_document)
                if result_compare.any() == True:
                    continue
                else:
                    logger.info(
                        "Documento mais recente registrado no mongo - data registrada: {}".format(row.iloc[0]))
                    # Se a quantidade for -1, não há documentos para serem carregados
                    logger.info(
                        "Quantidade de documentos que serão carregados: {}, se -1, não há novos dados.".format(idx-1))
                    break

        except ValueError as error:
            print(error)
            logger.error(
                "Normalmente o error acontece porque os nomes do indexes das Series comparadas estão diferentes."
            )

        return self.list_update_new_data

    def update_mongo(self) -> None:
        """Método que atualiza o MongoDB com as informações preparadas no método dados_para_upload."""
        self.list_update_new_data.pop()
        if bool(self.dict_rename) == False:
            raise ValueError(
                "O dicionário está vazio, não foi criado corretamente!")

        if not self.list_update_new_data:
            logger.debug(
                "A lista de dicionários utilizada para atualizar os dados no mongo está vazia.")

        else:
            logger.info("escrevendo na collection %s", self.collection)
            self.collection.insert_many(self.list_update_new_data)
