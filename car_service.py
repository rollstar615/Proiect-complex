from domain.car import Car
from repository.car_repository import CarInMemoryRepository


class CarService:
    """
    Manages car logic.
    """

    def __init__(self, repository, order_repository, validator):
        """
        Creates a car service.
        """
        self.__repository = repository
        self.__order_repository = order_repository
        self.__validator = validator

        self.__undo_operations = []

    def add_car(self, id_car, indicator, comfort_level, card_payment, model):
        """
        Creates a car
        :param id_car: int, the card id.
        :param indicator: int, the indicator.
        :param comfort_level: str, one of 'standard', 'high', 'premium'
        :param card_payment: bool
        :param model: str, the model
        """
        if card_payment == 'da':
            card_payment = True
        else:
            card_payment = False
        car = Car(id_car, indicator, comfort_level, card_payment, model)
        self.__validator.validate(car)
        self.__repository.create(car)

        self.__undo_operations.append(lambda: self.__repository.delete(car.id_entity))

    def __id_car_exists_in_orders(self, id_car):
        for order in self.__order_repository.read():
            if order.id_car == id_car:
                return True
        return False

    def remove_car(self, id_car):
        # ok si fara if, dar atunci trebuie prinsa exceptia pe UI
        if self.__id_car_exists_in_orders(id_car):
            # TODO: custom error class
            raise ValueError('Masina face parte din cel putin o comanda si nu poate fi stearsa!')
        car_to_delete = self.__repository.read(id_car)
        if car_to_delete is not None:
            self.__repository.delete(id_car)
            self.__undo_operations.append(lambda: self.__repository.create(car_to_delete))

    def update_car(self, id_car,indicator, comfort_level, card_payment, model):
        car_to_update=self.__repository.read(id_car)
        if car_to_update is not None:
            if card_payment == 'da':
                card_payment = True
            else:
                card_payment = False
            car = Car(id_car, indicator, comfort_level, card_payment, model)
            self.__repository.update(car)

    def get_all(self):
        """
        :return: a list of all the cars.
        """
        return self.__repository.read()

    def get_sorted_by_model(self):
        return sorted(self.get_all(),
                      key=lambda car: car.model,
                      reverse=True)

    def undo(self):
        if len(self.__undo_operations) > 0:
            undo_op = self.__undo_operations.pop()
            undo_op()
