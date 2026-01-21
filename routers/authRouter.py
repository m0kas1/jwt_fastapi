from fastapi import APIRouter
from fastapi.params import Depends
from conrollers.authController import authController
from dependencies import proverka_token

router = APIRouter()
auth_controller = authController()

router.add_api_route("/login",
    auth_controller.login,
    methods=["POST"])
router.add_api_route("/registration",
    auth_controller.registration,
    methods=["POST"])
router.add_api_route("/logout",
    auth_controller.getAll,
    methods=["POST"])
router.add_api_route("/users",
    auth_controller.getAll,
    dependencies=[Depends(proverka_token)],
    methods=["GET"])
router.add_api_route("/refresh",
    auth_controller.getAll,
    methods=["GET"])