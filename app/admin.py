from werkzeug import check_password_hash, generate_password_hash
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

# Admin Dashboard Controls
class Controller(ModelView):
	def is_accessible(self):
		''' validate if user is logged in and have admin role to access admin panel '''
		access = False
		print 
		if current_user.is_authenticated and current_user.isadmin == True:
			access = True
		return access

class UserModelView(Controller):
	''' encrypting password entered from admin panel '''
	def on_model_change(self, form, model, is_created):
		if 'pbkdf2:sha256:' not in model.password_hash:
			model.password_hash = generate_password_hash(model.password_hash)

class TeamModelView(Controller):
	''' excluding players from admin team adding interface '''
	form_excluded_columns = ('players')		
