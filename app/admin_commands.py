from vk_events import send_message
from create_db import engine, get_session, guests, orgs, groups, info, tech_support, sendings


def is_commands(user_id, event, text, vk_session, is_admin):

    if text == "/commands":

        if is_admin(user_id, event):

            send_message(vk_session, user_id, "/get_mailings показать список рассылок")
            send_message(vk_session, user_id,
                         "/start_mailing name first_group third_group ninth_group ... и так далее через пробел, где name - имя рассылки, а first_group, second_group... группы пользователей, в которых должно стоять значение True.\nНапример, чтобы запустить рассылку с именем 'test' для тех, кто оплатил билет и подписался на бота в тг, нужно ввести команду\n'/start_mailing test first_group twelfth_group', а для тех, кто просто оплатил билет,\n'/start_mailing test first_group'")
            send_message(vk_session, user_id,
                         "/give_level id True/False first_group third_group ninth_group ... и так далее через пробел, где first_group, second_group... группы пользователей, в которых должно стоять значение True, id -  айди пользователя")
            send_message(vk_session, user_id,
                         "/get_members first_group third_group ninth_group ..., и так далее через пробел, где first_group, second_group... группы пользователей, в которых должно стоять значение True.")
            send_message(vk_session, user_id, "/get_orgs показать список всех организаторов")
            send_message(vk_session, user_id, "/get_unread показать список непрочитанных сообщений ботом")
            send_message(vk_session, user_id, "/get_members_all - список всех участников (нерекомендуемая команда)")
            send_message(vk_session, user_id,
                         "/start_mailing_all name, где name имя рассылки. Начинает всеобщую спам-атаку.")

        else:

            send_message(vk_session, user_id, "No permission!")

    if text == "/get_mailings":

        if is_admin(user_id, event):

            send_message(vk_session, user_id, "Mailing list:")
            session = get_session(engine)

            query = session.query(sendings)

            for row in query:

                message = f"{str(row.mail_name)}\n{str(row.send_time)}\n{str(row.group_num)}\n\n{str(row.text)}\n\n{str(row.media)}"
                send_message(vk_session, user_id, message)

        else:

            send_message(vk_session, user_id, "No permission!")

    if text[:19] == "/start_mailing_all ":

        if is_admin(user_id, event):

            message = text.split()
            session = get_session(engine)
            query_s = session.query(sendings)
            ind = 0

            for row_s in query_s:

                if row_s.mail_name.lower() == message[1]:

                    query_org = session.query(guests)
                    ind = 1

                    for row_org in query_org:
                        guest_id = row_org.vk_link.split('/')[3][2:]
                        send_message(vk_session, guest_id, row_s.text)

                    send_message(vk_session, user_id, "Mailing done!")

                    break

            if ind == 0:
                send_message(vk_session, user_id, "Mailing name not found!")

        else:

            send_message(vk_session, user_id, "No permission!")

    if text[:15] == "/start_mailing ":

        if is_admin(user_id, event):

            message = text.split()
            session = get_session(engine)
            levels = ["first_group", "second_group", "third_group", "fourth_group", "fifth_group",
                       "sixth_group", "seventh_group", "eighth_group", "ninth_group", "tenth_group", "eleventh_grup",
                       "twelfth_group", "thirteenth_group"]
            flag = 0
            for i in range(2, len(message)):
                if int(message[i]) >= 14 or int(message[i]) <= 0:
                    flag = 1

            if flag == 0:

                query_s = session.query(sendings)
                ind = 0

                for row_s in query_s:

                    if row_s.mail_name.lower() == message[1]:

                        query_org = session.query(guests)
                        ind = 1

                        for row_org in query_org:

                            flag = 0

                            for i in range(2, len(message)):

                                if str(getattr(row_org, levels[message[i]], True)) != "True":
                                    flag = 1

                            if flag == 0:
                                guest_id = row_org.vk_link.split('/')[3][2:]
                                send_message(vk_session, guest_id, row_s.text)

                        send_message(vk_session, user_id, "Mailing done!")

                        break

                if ind == 0:
                    send_message(vk_session, user_id, "Mailing name not found!")

            else:

                send_message(vk_session, user_id, "Invalid command!")

        else:

            send_message(vk_session, user_id, "No permission!")

    if text[:12] == "/give_level ":

        if is_admin(user_id, event):

            message = text.split()
            session = get_session(engine)
            levels = ["first_group", "second_group", "third_group", "fourth_group", "fifth_group", "sixth_group",
                       "seventh_group", "eighth_group", "ninth_group", "tenth_group", "eleventh_grup",
                       "twelfth_group", "thirteenth_group", "true", "false"]

            flag = 0
            for i in range(2, len(message)):
                if int(message[i]) >= 14 or int(message[i]) <= 0:
                    flag = 1

            if flag == 0:

                try:

                    query = session.query(guests).get(int(message[1]))
                    ind = 0

                    for i in range(3, len(message)):

                        ind = 1
                        setattr(query, message[i], eval(message[2].capitalize()))

                    if ind == 1:

                        session.add(query)
                        session.commit()
                        send_message(vk_session, user_id, "Done!")

                    else:

                        send_message(vk_session, user_id, "Invalid command!")

                except BaseException:
    
                    send_message(vk_session, user_id, "Invalid command!")

            else:

                send_message(vk_session, user_id, "Invalid command!")

        else:

            send_message(vk_session, user_id, "No permission!")

    if text == "/get_members_all":

        if is_admin(user_id, event):

            session = get_session(engine)
            query = session.query(guests)

            for row in query:
                stroka = str(row.id) + " " + str(row.name) + " " + str(row.surname) + "\n" + str(
                    row.vk_link) + "\n\n" + "Написал боту:" + str(row.first_group) + "\n\n" + "Вступил в группу:" + str(
                    row.second_group) + "\n\n" + "Зарегистрировался:" + str(row.third_group) + "\n\n" + "Оплатил:" + str(
                    row.fourth_group) + "\n\n" + "Отметил в форме трансфера - Парк победы:" + str(
                    row.fifth_group) + "\n\n" + "Отметил в форме трансфера - Одинцово:" + str(
                    row.sixth_group) + "\n\n" + "Отметил в форме трансфера - самостоятельно:" + str(
                    row.seventh_group) + "\n\n" + "Прошел форму на расселение:" + str(
                    row.eighth_group) + "\n\n" + "Согласовал ли трансфер:" + str(
                    row.ninth_group) + "\n\n" + "Согласовал ли расселение:" + str(
                    row.tenth_group) + "\n\n" + "Заказал мерч:" + str(
                    row.eleventh_grup) + "\n\n" + "Подписался на бота в ТГ:" + str(
                    row.twelfth_group) + "\n\n" + "Вернул ли билет:" + str(row.thirteenth_group)
                send_message(vk_session, user_id, stroka)

        else:

            send_message(vk_session, user_id, "No permission!")

    if text[:13] == "/get_members ":

        if is_admin(user_id, event):

            session = get_session(engine)
            message = text.split()
            levels = ["/get_members", "first_group", "second_group", "third_group", "fourth_group", "fifth_group",
                       "sixth_group", "seventh_group", "eighth_group", "ninth_group", "tenth_group", "eleventh_grup",
                       "twelfth_group", "thirteenth_group"]
            flag = 0

            for i in message:
                if not (i in levels):
                    flag = 1

            if flag == 0:

                query = session.query(guests)
                ind = 0

                for row in query:

                    flag = 0

                    for i in message:

                        if str(getattr(row, i, True)) != "True":
                            flag = 1

                    if flag == 0:
                        ind = 1
                        stroka = str(row.id) + " " + str(row.name) + " " + str(row.surname) + "\n" + str(
                            row.vk_link) + "\n\n" + "Написал боту:" + str(
                            row.first_group) + "\n\n" + "Вступил в группу:" + str(
                            row.second_group) + "\n\n" + "Зарегистрировался:" + str(
                            row.third_group) + "\n\n" + "Оплатил:" + str(
                            row.fourth_group) + "\n\n" + "Отметил в форме трансфера - Парк победы:" + str(
                            row.fifth_group) + "\n\n" + "Отметил в форме трансфера - Одинцово:" + str(
                            row.sixth_group) + "\n\n" + "Отметил в форме трансфера - самостоятельно:" + str(
                            row.seventh_group) + "\n\n" + "Прошел форму на расселение:" + str(
                            row.eighth_group) + "\n\n" + "Согласовал ли трансфер:" + str(
                            row.ninth_group) + "\n\n" + "Согласовал ли расселение:" + str(
                            row.tenth_group) + "\n\n" + "Заказал мерч:" + str(
                            row.eleventh_grup) + "\n\n" + "Подписался на бота в ТГ:" + str(
                            row.twelfth_group) + "\n\n" + "Вернул ли билет:" + str(row.thirteenth_group)
                        send_message(vk_session, user_id, stroka)

                if ind == 0:
                    send_message(vk_session, user_id, "No results!")

            else:

                send_message(vk_session, user_id, "Invalid command!")

        else:

            send_message(vk_session, user_id, "No permission!")

    if text == "/get_orgs":

        if is_admin(user_id, event):

            send_message(vk_session, user_id, "Orgs list:")
            session = get_session(engine)
            query = session.query(orgs)

            for row in query:
                stroka = str(row.id) + " " + str(row.name) + " " + str(row.surname) + " \n" + str(row.vk_org_link)
                send_message(vk_session, user_id, stroka)

        else:

            send_message(vk_session, user_id, "No permission!")

    if text == "/get_unread":

        if is_admin(user_id, event):

            conversation_inf = vk_session.method("messages.getConversations", {"filter": "unread"})
            send_message(vk_session, user_id, "Unread messages:")

            for i in conversation_inf["items"]:
                if i["last_message"]["from_id"] != user_id:
                    message = f"https://vk.com/id{str(i['last_message']['from_id'])}\n{str(i['last_message']['text'])}"
                    send_message(vk_session, user_id, message)

        else:

            send_message(vk_session, user_id, "No permission!")
