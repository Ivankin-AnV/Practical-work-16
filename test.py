from main import CoffeeOrderBuilder

if __name__ == "__main__":
    # Тест базового заказа
    builder = CoffeeOrderBuilder()
    order = (
        builder
        .set_base("latte")
        .set_size("medium")
        .set_milk("oat")
        .add_syrup("vanilla")
        .set_sugar(2)
        .set_iced()
        .build()
    )
    assert order.base == "latte"
    assert order.size == "medium"
    assert order.milk == "oat"
    assert "vanilla" in order.syrups
    assert order.sugar == 2
    assert order.iced is True
    assert order.price > 0
    assert "medium latte with oat milk +vanilla (iced) 2 tsp sugar" == str(order)
    
    # Тест повторного использования билдера
    order1 = builder.build()
    builder.set_base("espresso").set_size("small")
    order2 = builder.build()
    assert order1.base == "latte"  # Не изменился
    assert order2.base == "espresso"
    assert order1.price != order2.price
    
    # Тесты валидации
    try:
        CoffeeOrderBuilder().build()
        assert False
    except ValueError:
        pass
    
    try:
        CoffeeOrderBuilder().set_base("latte").build()
        assert False
    except ValueError:
        pass
    
    try:
        CoffeeOrderBuilder().set_size("medium").build()
        assert False
    except ValueError:
        pass
    
    try:
        builder.set_sugar(6).build()
        assert False
    except ValueError:
        pass
    
    # Тест дублирования сиропов
    builder.clear_extras().set_base("americano").set_size("large").add_syrup("caramel").add_syrup("caramel")
    order_dup = builder.build()
    assert len(order_dup.syrups) == 1
    assert order_dup.price == (250 * 1.4) + 0 + 40 + 0  # Нет доплаты за дубликат
    
    # Тест цены за лед
    builder.clear_extras().set_base("espresso").set_size("small").set_iced()
    order_iced = builder.build()
    assert order_iced.price == (200 * 1.0) + 0 + 0 + 0.2
    
    print("All tests passed!")