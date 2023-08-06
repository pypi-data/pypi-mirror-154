#om_api

Это библиотека с набором функций для работы с Optomacros API
В библиотеке есть функции:
- [make_request](#make_request)
- [DataFrame_to_List](#DataFrame_to_List)
- [get_properties](#get_properties)
- [get_list](#get_list)
- [get_parents](#get_parents)
- [get_items](#get_items)
- [get_items_under_parent](#get_items_under_parent)
- [add_item_to_list](#add_item_to_list)
- [change_properties](#change_properties)
- [add_item_with_properties](#add_item_with_properties)

## make_request
`make_request(request_type: str, param: dict = ..., data: dict = ...)`
Позволяет отправлять запросы к API Optimacros
Реализованы методы : `get`, `post`
Для корректной работы функции обязательно предварительное создание констант: 
- `SERVICE` Содержащую alias сервиса к которому мы будем обращаться
- `URL` Содержащую адрес к которому мы будем обращаться в формате строки https://***/api/v1/service/{SERVICE}
- `COOKIE` {'token' : "ваш токен"}
    Времненный токен можно достать нажав `f12` в браузере и в cookie будет храниться ваш токен

## DataFrame_to_List

## get_properties

## get_list

## get_parents

## get_items

## get_items_under_parent

## add_item_to_list

## change_properties

## add_item_with_properties