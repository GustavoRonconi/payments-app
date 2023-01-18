<br />
<p align="center">
  <a href="https://kanastra.com.br/en/">
    <img src="https://grao.vc/wp-content/uploads/2022/12/kanastra_crunchbase_logo_verde.png" alt="Logo" width="300" height="300">
  </a>


  <h3 align="center">Kanastra - Challenge</h3>
</p>



### Construído a partir de:

* [Django](https://www.djangoproject.com/)
* [Postgrees](https://postgrees.org)


## Iniciando

Crie um ambiente python-3.10 e instale as dependências, presume-se neste ponto que você já tenha o Postgres instalado no seu ambiente.

### Pré-requisitos
* django==4.1.5
* djangorestframework==3.14.0
* djangorestframework_simplejwt==5.2.2
* pytest-django==4.5.2
* pytest-cov==4.0.0
* pytest==7.2.1
* requests==2.28.2
* gunicorn==20.1.0
* pyyaml==6.0
* uritemplate==4.1.1
* django-rest-swagger==2.2.0
* pandas==1.5.2
* psycopg2==2.9.5
* psycopg2-binary==2.9.5
* boto3==1.26.51

### Instalação
1. Clone o projeto e na pasta raiz execute:
   ```bash
   pip install -r requirements.txt
   ```

2. Rode o seguinte comando na pasta raiz:
    ```bash
    make install
    ```


## Utilização
1. Para iniciar a API no ambiente de desenvolvimento execute:
   ```python
   python manage.py runserver 
   ```
2. Credenciais para autenticação:
   - username: gustavoronconi
   - password: kanastra
