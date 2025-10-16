"""Потребитель RabbitMQ для сервиса рассылки"""  # pylint: disable=W1203, E0401, W0718, C0301
import json
import logging
import aio_pika
import traceback
from shared.messaging.consumers import BaseConsumer
from mailing_service.celery_mail.tasks import process_notification_task



logger = logging.getLogger(__name__)

class MailingConsumer(BaseConsumer):
    """Потребитель для обработки уведомлений и отправки email через Celery"""

    def __init__(self, rabbitmq_url: str, exchange_name: str = "auth_exchange"):
        super().__init__(rabbitmq_url, exchange_name)
        self.queue_name = "mailing_queue"
        self.consumer_id = id(self)  # Уникальный ID для отладки

    async def setup_queues(self):
        """Настройка очередей для mailing service"""
        print(f"🎯 [CONSUMER {self.consumer_id}] STARTING setup_queues()")

        queue = await self.declare_and_bind_queue(
            queue_name=self.queue_name,
            routing_key="notification.*"
        )
        await queue.consume(self.handle_notification)

        print(f"✅ [CONSUMER {self.consumer_id}] setup_queues() COMPLETED")
        print(f"✅ [CONSUMER {self.consumer_id}] Listening on: {self.queue_name}")
        print(f"✅ [CONSUMER {self.consumer_id}] Exchange: {self.exchange_name}")
        print(f"✅ [CONSUMER {self.consumer_id}] Routing: notification.*")

    async def handle_notification(self, message: aio_pika.IncomingMessage):
        """Обработка входящих уведомлений"""
        print("📨 NEW MESSAGE RECEIVED:")
        print(f"   Routing Key: {message.routing_key}")
        print(f"   Message ID: {message.message_id}")
        print(f"   Body: {message.body.decode()}")

        try:
            success = await self.process_message(message, self._process_notification)
            if success:
                print("✅ Notification processed successfully")
            else:
                print("❌ Failed to process notification")
        except Exception as e:
            print(f"💥 Error in handle_notification: {e}")
            traceback.print_exc()

    async def _process_notification(self, message: aio_pika.IncomingMessage):
        """Основная логика обработки уведомления - теперь через Celery"""
        body = json.loads(message.body.decode())
        print(f"Received notification: {body}")

        notification_type = body.get("type")
        user_email = body.get("user_email")
        user_id = body.get("user_id")
        data = body.get("data", {})

        if not user_email or not user_id:
            logger.error("No user_email or user_id in notification")
            return

        # Создаем данные для Celery задачи
        celery_data = {
            "user_id": user_id,
            "user_email": user_email,
            "type": notification_type,
            "data": data
        }

        # Добавляем subject и content
        celery_data["subject"] = self._get_subject_by_type(notification_type, data)
        celery_data["content"] = self._get_content_by_type(notification_type, data)
        celery_data["html_content"] = self._create_html_content(notification_type, data)

        # Отправляем задачу в Celery
        task = process_notification_task.delay(celery_data)

        print(f"Celery task created: {task.id} for notification type: {notification_type}")

    def _create_html_content(self, notification_type: str, data: dict) -> str:
        """Создание HTML контента для email"""
        username = data.get("username", "Пользователь")

        match notification_type:
            case "user_registered":
                return self._create_welcome_template(username)

            case "role_approved":
                return self._create_role_approved_template(username, data)

            case "role_rejected":
                return self._create_role_rejected_template(username, data)

            case _:
                logger.warning(f"Unknown notification type: {notification_type}")
                return self._create_custom_template("У вас новое уведомление.")

    def _get_subject_by_type(self, notification_type: str, data: dict) -> str:
        """Получение темы сообщения по типу уведомления"""
        subjects = {
            "user_registered": "Добро пожаловать на платформу!",
            "role_approved": "Положительный ответ на вашу заявку.",
            "role_rejected": "Отрицательный ответ на вашу заявку.",
            "custom_notification": data.get("subject", "Уведомление от CFDChamp")
        }
        return subjects.get(notification_type, "Уведомление от CFDChamp")

    def _get_content_by_type(self, notification_type: str, data: dict) -> str:
        """Получение текста сообщения по типу уведомления"""
        username = data.get("username", "Пользователь")
        custom_content = data.get("content", "")

        contents = {
            "user_registered": f"""Добро пожаловать, {username}!
                    Спасибо за регистрацию на нашем ресурсе.""",
            "role_approved": f"Уважаемый {username}! Ваша новая роль подтверждена администратором",
            "role_rejected": f"Уважаемый {username}! Ваша новая роль отклонена администратором",
            "custom_notification": custom_content or "У вас новое уведомление."
        }
        return contents.get(notification_type, "У вас новое уведомление.")

    def _create_welcome_template(self, username: str) -> str:
        """Красивый шаблон приветственного письма"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            </style>
        </head>
        <body style="font-family: 'Inter', Arial, sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div style="max-width: 500px; margin: 40px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.1);">
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #4F46E5 0%, #7E22CE 100%); padding: 40px 30px; text-align: center;">
                    <div style="background: white; width: 80px; height: 80px; border-radius: 20px; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
                        <span style="font-size: 32px; color: #4F46E5;">🎯</span>
                    </div>
                    <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700;">Добро пожаловать!</h1>
                    <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0; font-size: 16px; font-weight: 400;">{username}, начинаем торговое путешествие</p>
                </div>
                
                <!-- Content -->
                <div style="padding: 40px 30px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h2 style="color: #1F2937; margin: 0 0 15px; font-size: 22px; font-weight: 600;">Ваш аккаунт активирован</h2>
                        <p style="color: #6B7280; margin: 0; line-height: 1.6;">Теперь вы часть сообщества профессиональных трейдеров CFDChamp</p>
                    </div>
                    
                    <!-- Features -->
                    <div style="background: #F8FAFC; border-radius: 12px; padding: 25px; margin: 30px 0;">
                        <h3 style="color: #374151; margin: 0 0 20px; font-size: 16px; font-weight: 600; text-align: center;">Доступные возможности</h3>
                        <div style="display: grid; gap: 15px;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="background: #4F46E5; width: 8px; height: 8px; border-radius: 50%;"></div>
                                <span style="color: #4B5563; font-size: 14px;">Анализ CFD инструментов в реальном времени</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="background: #7E22CE; width: 8px; height: 8px; border-radius: 50%;"></div>
                                <span style="color: #4B5563; font-size: 14px;">Точные торговые сигналы и аналитика</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="background: #10B981; width: 8px; height: 8px; border-radius: 50%;"></div>
                                <span style="color: #4B5563; font-size: 14px;">Образовательные материалы и вебинары</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="background: #F59E0B; width: 8px; height: 8px; border-radius: 50%;"></div>
                                <span style="color: #4B5563; font-size: 14px;">Персональная поддержка 24/7</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- CTA Button -->
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="#" style="display: inline-block; background: linear-gradient(135deg, #4F46E5, #7E22CE); color: white; padding: 14px 32px; text-decoration: none; border-radius: 12px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3); transition: all 0.3s;">
                            Начать торговать
                        </a>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="background: #F8FAFC; padding: 25px 30px; text-align: center; border-top: 1px solid #E5E7EB;">
                    <p style="color: #6B7280; margin: 0 0 10px; font-size: 14px;">Нужна помощь? Мы всегда на связи</p>
                    <p style="color: #9CA3AF; margin: 0; font-size: 12px;">
                        С уважением, команда CFDChamp<br>
                        <span style="color: #D1D5DB;">© 2024 CFDChamp. Все права защищены.</span>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

    def _create_role_approved_template(self, username: str, data: dict) -> str:
        """Красивый шаблон для уведомления об одобрении роли"""
        new_role = data.get("new_role", "новая роль")
        role_description = data.get("role_description", "дополнительные возможности платформы")

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            </style>
        </head>
        <body style="font-family: 'Inter', Arial, sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #10B981 0%, #059669 100%);">
            <div style="max-width: 500px; margin: 40px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.1);">
                <!-- Success Header -->
                <div style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); padding: 40px 30px; text-align: center;">
                    <div style="background: white; width: 80px; height: 80px; border-radius: 20px; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
                        <span style="font-size: 32px; color: #10B981;">✅</span>
                    </div>
                    <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700;">Роль одобрена!</h1>
                    <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0; font-size: 16px; font-weight: 400;">Поздравляем с новыми возможностями</p>
                </div>
                
                <!-- Content -->
                <div style="padding: 40px 30px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h2 style="color: #1F2937; margin: 0 0 10px; font-size: 22px; font-weight: 600;">Приветствуем, {username}!</h2>
                        <p style="color: #6B7280; margin: 0; line-height: 1.6;">Ваш запрос на роль <strong style="color: #10B981;">{new_role}</strong> успешно одобрен</p>
                    </div>
                    
                    <!-- Role Benefits -->
                    <div style="background: #ECFDF5; border: 1px solid #D1FAE5; border-radius: 12px; padding: 25px; margin: 30px 0;">
                        <h3 style="color: #065F46; margin: 0 0 15px; font-size: 16px; font-weight: 600; text-align: center;">🎉 Новые возможности</h3>
                        <p style="color: #047857; margin: 0; text-align: center; font-size: 14px; line-height: 1.5;">
                            {role_description}
                        </p>
                    </div>
                    
                    <!-- Next Steps -->
                    <div style="background: #F8FAFC; border-radius: 12px; padding: 20px; margin: 25px 0;">
                        <h4 style="color: #374151; margin: 0 0 15px; font-size: 14px; font-weight: 600;">Что дальше?</h4>
                        <div style="display: grid; gap: 12px;">
                            <div style="display: flex; align-items: start; gap: 10px;">
                                <span style="color: #10B981; font-size: 12px;">▶</span>
                                <span style="color: #4B5563; font-size: 13px;">Войдите в свой аккаунт для доступа к новым функциям</span>
                            </div>
                            <div style="display: flex; align-items: start; gap: 10px;">
                                <span style="color: #10B981; font-size: 12px;">▶</span>
                                <span style="color: #4B5563; font-size: 13px;">Изучите обновленный интерфейс платформы</span>
                            </div>
                            <div style="display: flex; align-items: start; gap: 10px;">
                                <span style="color: #10B981; font-size: 12px;">▶</span>
                                <span style="color: #4B5563; font-size: 13px;">Обратитесь к поддержке при возникновении вопросов</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- CTA Button -->
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="#" style="display: inline-block; background: linear-gradient(135deg, #10B981, #059669); color: white; padding: 14px 32px; text-decoration: none; border-radius: 12px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);">
                            Перейти в платформу
                        </a>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="background: #F8FAFC; padding: 25px 30px; text-align: center; border-top: 1px solid #E5E7EB;">
                    <p style="color: #6B7280; margin: 0 0 10px; font-size: 14px;">Рады видеть вас в нашем сообществе</p>
                    <p style="color: #9CA3AF; margin: 0; font-size: 12px;">
                        С уважением, команда CFDChamp<br>
                        <span style="color: #D1D5DB;">© 2024 CFDChamp. Все права защищены.</span>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

    def _create_role_rejected_template(self, username: str, data: dict) -> str:
        """Красивый шаблон для уведомления об отклонении роли"""
        requested_role = data.get("requested_role", "запрашиваемая роль")
        reason = data.get("reason", "Требования к роли не выполнены")
        contact_support = data.get("contact_support", True)

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            </style>
        </head>
        <body style="font-family: 'Inter', Arial, sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);">
            <div style="max-width: 500px; margin: 40px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.1);">
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%); padding: 40px 30px; text-align: center;">
                    <div style="background: white; width: 80px; height: 80px; border-radius: 20px; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
                        <span style="font-size: 32px; color: #EF4444;">❌</span>
                    </div>
                    <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700;">Запрос отклонен</h1>
                    <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0; font-size: 16px; font-weight: 400;">{username}, ваш запрос рассмотрен</p>
                </div>
                
                <!-- Content -->
                <div style="padding: 40px 30px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h2 style="color: #1F2937; margin: 0 0 15px; font-size: 22px; font-weight: 600;">К сожалению, роль не одобрена</h2>
                        <p style="color: #6B7280; margin: 0; line-height: 1.6;">Запрос на роль <strong style="color: #EF4444;">{requested_role}</strong> был отклонен</p>
                    </div>
                    
                    <!-- Reason -->
                    <div style="background: #FEF2F2; border: 1px solid #FECACA; border-radius: 12px; padding: 25px; margin: 30px 0;">
                        <h3 style="color: #7F1D1D; margin: 0 0 15px; font-size: 16px; font-weight: 600; text-align: center;">📋 Причина отказа</h3>
                        <p style="color: #B91C1C; margin: 0; text-align: center; font-size: 14px; line-height: 1.5;">
                            {reason}
                        </p>
                    </div>
                    
                    <!-- Next Steps -->
                    <div style="background: #F8FAFC; border-radius: 12px; padding: 20px; margin: 25px 0;">
                        <h4 style="color: #374151; margin: 0 0 15px; font-size: 14px; font-weight: 600;">Возможные действия</h4>
                        <div style="display: grid; gap: 12px;">
                            <div style="display: flex; align-items: start; gap: 10px;">
                                <span style="color: #EF4444; font-size: 12px;">▶</span>
                                <span style="color: #4B5563; font-size: 13px;">Ознакомьтесь с требованиями к запрашиваемой роли</span>
                            </div>
                            <div style="display: flex; align-items: start; gap: 10px;">
                                <span style="color: #EF4444; font-size: 12px;">▶</span>
                                <span style="color: #4B5563; font-size: 13px;">Улучшите ваш профиль и активность на платформе</span>
                            </div>
                            <div style="display: flex; align-items: start; gap: 10px;">
                                <span style="color: #EF4444; font-size: 12px;">▶</span>
                                <span style="color: #4B5563; font-size: 13px;">Подайте новый запрос через 30 дней</span>
                            </div>
                            {"<div style='display: flex; align-items: start; gap: 10px;'><span style='color: #EF4444; font-size: 12px;'>▶</span><span style='color: #4B5563; font-size: 13px;'>Свяжитесь с поддержкой для уточнения деталей</span></div>" if contact_support else ""}
                        </div>
                    </div>
                    
                    <!-- Support CTA -->
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="#" style="display: inline-block; background: linear-gradient(135deg, #EF4444, #DC2626); color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 14px; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3); margin: 0 5px;">
                            Связаться с поддержкой
                        </a>
                        <a href="#" style="display: inline-block; background: #6B7280; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 14px; margin: 0 5px;">
                            Требования к ролям
                        </a>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="background: #F8FAFC; padding: 25px 30px; text-align: center; border-top: 1px solid #E5E7EB;">
                    <p style="color: #6B7280; margin: 0 0 10px; font-size: 14px;">Надеемся на ваше понимание</p>
                    <p style="color: #9CA3AF; margin: 0; font-size: 12px;">
                        С уважением, команда CFDChamp<br>
                        <span style="color: #D1D5DB;">© 2024 CFDChamp. Все права защищены.</span>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

    def _create_custom_template(self, content: str) -> str:
        """Шаблон для кастомных уведомлений"""
        return f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: #f8f9fa; padding: 20px; border-radius: 5px;">
                    {content}
                </div>
                <p style="color: #666; font-size: 12px; margin-top: 20px;">
                    С уважением,<br>Команда CFDChamp
                </p>
            </div>
        </body>
        </html>
        """
