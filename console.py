from domain.car import Car
from domain.car_validator import CarValidationError
from repository.repository_error import RepositoryError



class Console:

    def __init__(self, car_service, location_service, order_service):
        self.__car_service = car_service
        self.__location_service = location_service
        self.__order_service = order_service

    def __show_menu(self):
        print('1. Masini')
        print('2. Locatii')
        print('3. Comenzi')
        print('x. Exit')

    def run_console(self):

        while True:
            self.__show_menu()
            op = input('Optiune: ')
            if op == '1':
                self.__show_masini()
            elif op == '2':
                self.__show_locatii()
            elif op == '3':
                self.__show_comenzi()
            elif op == 'x':
                break
            else:
                print('Comanda invalida!')

    def __show_masini(self):

        while True:
            self.__show_menu_masini()
            op = input('Optiune: ')
            if op == '1':
                self.__handle_masini_add()
            elif op == '2':
                self.__handle_masini_remove()
            elif op=='3':
                self.__handle_car_update()
            elif op == '4':
                self.__show_list(self.__car_service.get_sorted_by_model())
            elif op == '5':
                self.__handle_masini_undo()
            elif op == 'a':
                self.__show_list(self.__car_service.get_all())
            elif op == 'b':
                break
            else:
                print('Comanda invalida!')

    def __show_menu_masini(self):
        print('--- Masini')
        print('1. Adauga')
        print('2. Sterge')
        print('3. Update')
        print('4. Sortate desc dupa model')
        print('5. Undo cars') # TODO: undo/redo should be global
        print('a. Afisare')
        print('b. Back')

    def __handle_masini_undo(self):
        self.__car_service.undo()

    def __handle_masini_add(self):
        try:
            id_car = int(input('ID-ul: '))
            indicator = int(input('Indicativul: '))
            comfort_level = input('Nivelul de comfort (standard, high, premium): ')
            card_payment = input('Plata cu cardul (da sau nu): ')
            model = input('Modelul: ')
            self.__car_service.add_car(
                id_car,
                indicator,
                comfort_level,
                card_payment,
                model
            )
            print('Masina a fost adaugata!')
        except RepositoryError as re:
            print('Eroare:', re)
        except CarValidationError as cve:
            print('Erori:')
            for error in cve.args[0]:
                print(error)

            #print('Avem erori:', ve)

    def __show_list(self, objects):
        for object in objects:
            print(object)

    def __show_locatii(self):
        while True:
            self.__show_menu_locatii()
            op = input('Optiune: ')
            if op == '1':
                self.__handle_locatii_add()
            if op=='2':
                self.__handle_locatii_remove()
            elif op=='3':
                self.__handle_location_update()
            elif op == '4':
                self.__show_list(self.__location_service.get_sorted_desc_by_notes_length())
            elif op == 'a':
                self.__show_list(self.__location_service.get_all())
            elif op == 'b':
                break
            else:
                print('Comanda invalida!')

    def __show_menu_locatii(self):
        print('--- Locatii')
        print('1. Adauga')
        print('2. Sterge')
        print('3. Update')
        print('4. Sortate desc dupa lungimea observatiilor')
        print('a. Afisare')
        print('b. Back')

    def __handle_locatii_add(self):
        try:
            id_location = int(input('ID-ul: '))
            street_name= input('Numele strazii: ')
            number = int(input('Numarul strazii: '))
            block = input('Scara: ')
            building = input('Cladirea: ')
            notes = input('Observatii: ')
            self.__location_service.add_location(
                id_location,
                street_name,
                number,
                block,
                building,
                notes
            )
            print('Locatia a fost adaugata!')
        except RepositoryError as re:
            print('Eroare:', re)


    def __show_comenzi(self):
        while True:
            self.__show_menu_comenzi()
            op = input('Optiune: ')
            if op == '1':
                self.__handle_comenzi_add()
            elif op=='2':
                self.__handle_orders_remove()
            elif op=='3':
                self.__handle_comenzi_update()
            elif op == '4':
                self.__show_list(self.__order_service.get_streets_ordered_desc_by_max_distances())
            elif op == 'a':
                self.__show_list(self.__order_service.get_all())
            elif op == 'b':
                break
            else:
                print('Comanda invalida!')

    def __show_menu_comenzi(self):
        print('--- Comenzi')
        print('1. Adauga')
        print('2. Sterge')
        print('3. Update')
        print('4. Strazi sortate desc dupa distanta maxima a unei comenzi')
        print('a. Afisare')
        print('b. Back')

    def __handle_comenzi_add(self):
        try:
            id_order = int(input('ID-ul comenzii: '))
            id_car = int(input('ID-ul masinii: '))
            id_location = int(input('ID-ul locatiei: '))
            final_time = int(input('Timpul final: '))
            km_cost = float(input('Costul per km: '))
            distance = int(input('Distanta parcursa: '))
            status = input('Starea comenzii: ')
            self.__order_service.add_order(
                id_order,
                id_car,
                id_location,
                final_time,
                km_cost,
                distance,
                status
            )
            print('Locatia a fost adaugata!')
        except ValueError as ve:
            print('Erori:')
            for error in ve.args[0]:
                print(error)

    def __handle_masini_remove(self):
        try:
            id_car = int(input('Dati id-ul de sters: '))
            self.__car_service.remove_car(id_car)
        except Exception:
            print('TODO better exception handling')

    def __handle_locatii_remove(self):
        try:
            id_location = int(input('dati idul de sters'))
            self.__location_service.remove_location(id_location)
        except Exception:
            self.__location_service.remove_location(id_location)

    def __handle_orders_remove(self):
        try:
            id_order=int(input('dati idul de sters'))
            self.__order_service.remove_order(id_order)
        except Exception:
            self.__order_service.remove_order(id_order)

    def __handle_car_update(self):
            id_car=int(input('dati idul'))
            indicator=int(input('dati indicativul'))
            comfort_level=input('dati comfortul')
            card_payment=input('dati cardul')
            model=input('dati modelul')
            self.__car_service.update_car(
                id_car,
                indicator,
                comfort_level,
                card_payment,
                model
            )
            print('Masina a fost adaugata!')

    def __handle_location_update(self):
        id_location=int(input('dati idul'))
        street_name=input('dati numele')
        number=int(input('dati numarul'))
        block=input('dati blocul')
        building=input('dati cladirea')
        notes=input('dati notes')
        self.__location_service.update_location(
            id_location,
            street_name,
            number,
            block,
            building,
            notes
        )
        print('locatia a fost modificata')


    def __handle_comenzi_update(self):
        id_order=int(input('dati orderul'))
        id_car=int(input('dati masina'))
        id_location=int(input('dati locatia'))
        final_time=int(input('dati timpul'))
        km_cost=int(input('dati km'))
        distance=int(input('dati distanta'))
        status=input('dati statusul')
        self.__order_service.update_order(
            id_order,
            id_car,
            id_location,
            final_time,
            km_cost,
            distance,
            status
        )
        print('orderul a fost actualizat')
