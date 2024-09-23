from flask import jsonify, request
from sqlalchemy.orm import Session
from werkzeug.exceptions import BadRequest
from app.src.application.repositories.user_repository import UserRepository
from app.src.application.usecases.create_user_usecase import CreateUserUsecase, InputDto

def setup_user_routes(app):

    @app.route('/api/users', methods=['POST'])
    def create_user():
        try:
            # Obter dados do JSON enviado pelo cliente
            data = request.get_json()

            # Validação básica
            if not data or 'name' not in data or 'email' not in data or 'password' not in data:
                raise BadRequest('Dados inválidos.')

            input_dto = InputDto(name=data.get("name"),
                                 email=data.get("email"),
                                 password=data.get("password"),
                                 cpf=data.get("cpf"),
                                 birthday=data.get("birthday"))
            
            session = Session()
            repository = UserRepository(session)
            usecase = CreateUserUsecase(repository)
            output_dto = usecase.execute(input_dto=input_dto)

            return jsonify(output_dto), 201  # 201 Created

        except BadRequest as e:
            return jsonify({'error': str(e)}), 400  # 400 Bad Request
        except Exception as e:
            return jsonify({'error': 'Erro ao criar usuário.'}), 500  # 500 Internal Server Error
        