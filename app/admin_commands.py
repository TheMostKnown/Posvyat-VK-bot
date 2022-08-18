from vk_events import send_message
from vk_tools import admin_add_info
from create_db import engine, get_session, guests, orgs, groups, info, tech_support, sendings


def is_commands(user_id, event, text, vk_session, is_admin):

    if text == "/commands":

        if is_admin(user_id, event):

            send_message(vk_session, user_id, "/get_mailings показать список рассылок")
            send_message(vk_session, user_id,
                         "/start_mailing name first_group third_group ninth_group ... и так далее через пробел, где name - имя рассылки, а first_group, second_group... группы пользователей, в которых должно стоять значение True.\nНапример, чтобы запустить рассылку с именем 'test' для тех, кто оплатил билет и подписался на бота в тг, нужно ввести команду\n'/start_mailing test first_group twelfth_group', а для тех, кто просто оплатил билет,\n'/start_mailing test first_group'")
            send_message(vk_session, user_id,
                         "/give_level id level True/False, где level - название группы (first_group, second_group..., но только одна группа на одну команду!), id -  айди пользователя")
            send_message(vk_session, user_id,
                         "/get_members first_group third_group ninth_group ..., и так далее через пробел, где first_group, second_group... группы пользователей, в которых должно стоять значение True.")
            send_message(vk_session, user_id, "/get_orgs показать список всех организаторов")
            send_message(vk_session, user_id, "/get_unread показать список непрочитанных сообщений ботом")
            send_message(vk_session, user_id, "/get_members_all - список всех участников (нерекомендуемая команда)")
            send_message(vk_session, user_id,
                         "/start_mailing_all name, где name имя рассылки. Начинает всеобщую спам-атаку.")
            send_message(vk_session, user_id,
                         "/add_info (guestion?) answer - добавить пользователю новую кнопку в его информационную клавиатуру, где в скобках название кнопки, далее ответ на вопрос из кнопки")

        else:

            send_message(vk_session, user_id, "No permission!")


def is_get_mailings(user_id, event, text, vk_session, is_admin):

    if text == "/get_mailings":

        if is_admin(user_id, event):

            send_message(vk_session, user_id, "Mailing list:")
            session = get_session(engine)

            #dff
            q = session.query(sendings)
            for c in q:
                session.delete(c)
            m1 = sendings(mail_name="1", text="dfejfejejefjefj")
            m2 = sendings(mail_name="2", text="dfejfejejefjefj")
            m3 = sendings(mail_name="3", text="dfejfejejefjefj")
            m4 = sendings(mail_name="4", text="dfejfejejefjefj")
            m5 = sendings(mail_name="5", text="dfejfejejefjefj")
            session.add_all([m1, m2, m3, m4, m5])
            session.commit()
            #dff

            q = session.query(sendings)

            for c in q:

                stroka = str(c.mail_name) + " " + str(c.send_time) + " " + str(c.group_num) + " \n\n" + str(c.text) + "\n\n" + str(c.media)
                send_message(vk_session, user_id, stroka)

        else:

            send_message(vk_session, user_id, "No permission!")


def is_start_mailing_all(user_id, event, text, vk_session, is_admin):

    if text[:19] == "/start_mailing_all ":

        if is_admin(user_id, event):

            message = text.split()
            session = get_session(engine)
            q = session.query(sendings)
            ind = 0

            for c in q:

                if c.mail_name.lower() == message[1]:

                    qq = session.query(guests)
                    ind = 1

                    for cc in qq:
                        guest_id = cc.vk_link.split('/')[3][2:]
                        send_message(vk_session, guest_id, c.text)

                    send_message(vk_session, user_id, "Mailing done!")

                    break

            if ind == 0:
                send_message(vk_session, user_id, "Mailing name not found!")

        else:

            send_message(vk_session, user_id, "No permission!")


def is_start_mailing(user_id, event, text, vk_session, is_admin):

    if text[:15] == "/start_mailing ":

        if is_admin(user_id, event):

            message = text.split()
            session = get_session(engine)
            groupps = ["/get_members", "first_group", "second_group", "third_group", "fourth_group", "fifth_group",
                       "sixth_group", "seventh_group", "eighth_group", "ninth_group", "tenth_group", "eleventh_grup",
                       "twelfth_group", "thirteenth_group"]
            flag = 0

            for i in range(2, len(message)):
                if not (message[i] in groupps):
                    flag = 1

            if flag == 0:

                q = session.query(sendings)
                ind = 0

                for c in q:

                    if c.mail_name.lower() == message[1]:

                        qq = session.query(guests)
                        ind = 1

                        for cc in qq:

                            flag = 0

                            for i in range(2, len(message)):

                                if str(getattr(cc, message[i], True)) != "True":
                                    flag = 1

                            if flag == 0:
                                guest_id = cc.vk_link.split('/')[3][2:]
                                send_message(vk_session, guest_id, c.text)

                        send_message(vk_session, user_id, "Mailing done!")

                        break

                if ind == 0:
                    send_message(vk_session, user_id, "Mailing name not found!")

            else:

                send_message(vk_session, user_id, "Invalid command!")

        else:

            send_message(vk_session, user_id, "No permission!")


def is_give_level(user_id, event, text, vk_session, is_admin):

    if text[:12] == "/give_level ":

        if is_admin(user_id, event):

            message = text.split()
            session = get_session(engine)

            try:

                q = session.query(guests).get(int(message[1]))
                groupps = ["first_group", "second_group", "third_group", "fourth_group", "fifth_group", "sixth_group",
                           "seventh_group", "eighth_group", "ninth_group", "tenth_group", "eleventh_grup",
                           "twelfth_group", "thirteenth_group"]

                if message[2] in groupps:

                    setattr(q, message[2], eval(message[3].capitalize()))
                    session.add(q)
                    session.commit()
                    send_message(vk_session, user_id, "Done!")

                else:

                    send_message(vk_session, user_id, "Invalid command!")

            except BaseException:

                send_message(vk_session, user_id, "Invalid command!")

        else:

            send_message(vk_session, user_id, "No permission!")


def is_get_members_all(user_id, event, text, vk_session, is_admin):

    if text == "/get_members_all":

        if is_admin(user_id, event):

            session = get_session(engine)
            q = session.query(guests)

            for c in q:
                stroka = str(c.id) + " " + str(c.name) + " " + str(c.surname) + "\n" + str(
                    c.vk_link) + "\n\n" + "Написал боту:" + str(c.first_group) + "\n\n" + "Вступил в группу:" + str(
                    c.second_group) + "\n\n" + "Зарегистрировался:" + str(c.third_group) + "\n\n" + "Оплатил:" + str(
                    c.fourth_group) + "\n\n" + "Отметил в форме трансфера - Парк победы:" + str(
                    c.fifth_group) + "\n\n" + "Отметил в форме трансфера - Одинцово:" + str(
                    c.sixth_group) + "\n\n" + "Отметил в форме трансфера - самостоятельно:" + str(
                    c.seventh_group) + "\n\n" + "Прошел форму на расселение:" + str(
                    c.eighth_group) + "\n\n" + "Согласовал ли трансфер:" + str(
                    c.ninth_group) + "\n\n" + "Согласовал ли расселение:" + str(
                    c.tenth_group) + "\n\n" + "Заказал мерч:" + str(
                    c.eleventh_grup) + "\n\n" + "Подписался на бота в ТГ:" + str(
                    c.twelfth_group) + "\n\n" + "Вернул ли билет:" + str(c.thirteenth_group)
                send_message(vk_session, user_id, stroka)

        else:

            send_message(vk_session, user_id, "No permission!")


def is_get_members(user_id, event, text, vk_session, is_admin):

    if text[:13] == "/get_members ":

        if is_admin(user_id, event):

            session = get_session(engine)
            message = text.split()
            groupps = ["/get_members", "first_group", "second_group", "third_group", "fourth_group", "fifth_group",
                       "sixth_group", "seventh_group", "eighth_group", "ninth_group", "tenth_group", "eleventh_grup",
                       "twelfth_group", "thirteenth_group"]
            flag = 0

            for i in message:
                if not (i in groupps):
                    flag = 1

            if flag == 0:

                q = session.query(guests)
                ind = 0

                for c in q:

                    flag = 0

                    for i in message:

                        if str(getattr(c, i, True)) != "True":
                            flag = 1

                    if flag == 0:
                        ind = 1
                        stroka = str(c.id) + " " + str(c.name) + " " + str(c.surname) + "\n" + str(
                            c.vk_link) + "\n\n" + "Написал боту:" + str(
                            c.first_group) + "\n\n" + "Вступил в группу:" + str(
                            c.second_group) + "\n\n" + "Зарегистрировался:" + str(
                            c.third_group) + "\n\n" + "Оплатил:" + str(
                            c.fourth_group) + "\n\n" + "Отметил в форме трансфера - Парк победы:" + str(
                            c.fifth_group) + "\n\n" + "Отметил в форме трансфера - Одинцово:" + str(
                            c.sixth_group) + "\n\n" + "Отметил в форме трансфера - самостоятельно:" + str(
                            c.seventh_group) + "\n\n" + "Прошел форму на расселение:" + str(
                            c.eighth_group) + "\n\n" + "Согласовал ли трансфер:" + str(
                            c.ninth_group) + "\n\n" + "Согласовал ли расселение:" + str(
                            c.tenth_group) + "\n\n" + "Заказал мерч:" + str(
                            c.eleventh_grup) + "\n\n" + "Подписался на бота в ТГ:" + str(
                            c.twelfth_group) + "\n\n" + "Вернул ли билет:" + str(c.thirteenth_group)
                        send_message(vk_session, user_id, stroka)

                if ind == 0:
                    send_message(vk_session, user_id, "No results!")

            else:

                send_message(vk_session, user_id, "Invalid command!")

        else:

            send_message(vk_session, user_id, "No permission!")


def is_get_orgs(user_id, event, text, vk_session, is_admin):

    if text == "/get_orgs":

        if is_admin(user_id, event):

            send_message(vk_session, user_id, "Orgs list:")
            session = get_session(engine)
            q = session.query(orgs)

            for c in q:
                stroka = str(c.id) + " " + str(c.name) + " " + str(c.surname) + " \n" + str(c.vk_org_link)
                send_message(vk_session, user_id, stroka)

        else:

            send_message(vk_session, user_id, "No permission!")


def is_get_unread(user_id, event, text, vk_session, is_admin):

    if text == "/get_unread":

        if is_admin(user_id, event):

            conversation_inf = vk_session.method("messages.getConversations", {"filter": "unread"})
            send_message(vk_session, user_id, "Unread messages:")

            for i in conversation_inf["items"]:
                if i["last_message"]["from_id"] != user_id:
                    stroka = "https://vk.com/id" + str(i["last_message"]["from_id"]) + "\n" + str(
                        i["last_message"]["text"])
                    send_message(vk_session, user_id, stroka)

        else:

            send_message(vk_session, user_id, "No permission!")

def is_info(user_id, event, text, vk_session, session, is_admin):

    if text.startswith("/add_info"):

        if is_admin(user_id, event):

            if (admin_add_info(session, text)):
                send_message(vk_session, user_id, "Вопрос добавлен")
            else:
                send_message(vk_session, user_id, "Не удалось добавить вопрос")
        else:
            send_message(vk_session, user_id, "No permission!")
