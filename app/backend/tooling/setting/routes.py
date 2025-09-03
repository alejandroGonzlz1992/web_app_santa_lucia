# import

# local import
from app.backend.endpoint.auth.auth import auth_route
from app.backend.endpoint.crud.base import crud_route
from app.backend.endpoint.crud.entities.users import user_route
from app.backend.endpoint.crud.entities.roles import roles_route
from app.backend.endpoint.crud.records.deduction import deduction_route
from app.backend.endpoint.crud.records.department import department_route
from app.backend.endpoint.crud.records.payment_date import payment_date_route
from app.backend.endpoint.crud.records.question import question_route
from app.backend.endpoint.crud.records.schedule import schedule_route
from app.backend.endpoint.service.profile.profile import profile_route
from app.backend.endpoint.service.profile.checkin import checkin_route
from app.backend.endpoint.service.requests.inability import inability_route
from app.backend.endpoint.service.requests.permission import permission_route
from app.backend.endpoint.service.transactions.bonus import bonus_route
from app.backend.endpoint.service.transactions.payroll import payroll_route
from app.backend.endpoint.service.transactions.settlement import settlement_route
from app.backend.endpoint.service.evaluation.evaluation import evaluation_route
from app.backend.endpoint.service.requests.reports import reports_route


# instance
route_list: list[object] = [auth_route, crud_route, reports_route, user_route, roles_route, deduction_route,
                            department_route, payment_date_route, question_route, schedule_route, profile_route,
                            checkin_route, inability_route, permission_route, bonus_route, payroll_route,
                            settlement_route, evaluation_route]
