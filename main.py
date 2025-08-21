# main.py
from views import menu_view
from services import loteria_service, ventas_service

def main():
    """Función principal que ejecuta el menú de la aplicación."""
    while True:
        opcion = menu_view.show_main_menu()

        if opcion == "1":
            loterias = loteria_service.get_all_loterias()
            menu_view.show_loterias_list(loterias)
            loteria_seleccionada = menu_view.get_loteria_selection(loterias)
            if loteria_seleccionada:
                opcion_mod = menu_view.show_modify_options()
                if opcion_mod == "1":
                    nuevo_valor = menu_view.get_numeric_input("Ingrese el nuevo valor por fracción: ")
                    if loteria_service.update_loteria_value(loteria_seleccionada, nuevo_valor):
                        print("Valor actualizado exitosamente!")
                    else:
                        print("No se pudo actualizar el valor.")
                elif opcion_mod == "2":
                    nueva_cantidad = menu_view.get_numeric_input("Ingrese la nueva cantidad de inventario por fraccion: ")
                    if loteria_service.update_loteria_inventory(loteria_seleccionada, nueva_cantidad):
                        print("Cantidad actualizada exitosamente!")
                    else:
                        print("No se pudo actualizar la cantidad.")
                elif opcion_mod == "3":
                    # Nota: Esta opción podría requerir un manejo más complejo si el modelo es una clase estricta
                    print("La opción 'Agregar nueva información' no es aplicable directamente con el modelo de clase Loteria de esta forma.")
                    print("Si desea añadir nuevos atributos, debería modificarse la clase Loteria.")
                menu_view.display_loteria_info(loteria_seleccionada)
            else:
                print("Operación cancelada o lotería no válida.")

        elif opcion == "2":
            nombre, fracciones, valor, inventario = menu_view.get_new_loteria_data()
            nueva_loteria = loteria_service.add_new_loteria(nombre, fracciones, valor, inventario)
            print("\n¡Lotería agregada exitosamente!")
            menu_view.display_loteria_info(nueva_loteria)

        elif opcion == "3":
            menu_view.display_all_loterias_detailed()

        elif opcion == "4":
            nombre_buscado = menu_view.get_loteria_name_to_search()
            loteria_encontrada = loteria_service.find_loteria_by_name(nombre_buscado)
            menu_view.display_search_result(loteria_encontrada)

        elif opcion == "5":
            # Menú de ventas
            while True:
                opcion_ventas = menu_view.show_ventas_menu()
                
                if opcion_ventas == "1":
                    # Registrar nueva venta
                    try:
                        id_loteria, cantidad_fracciones, nombre_cliente, nombre_vendedor = menu_view.get_venta_data()
                        nueva_venta = ventas_service.add_new_venta(id_loteria, cantidad_fracciones, nombre_cliente, nombre_vendedor)
                        print("\n¡Venta registrada exitosamente!")
                        menu_view.display_venta_info(nueva_venta)
                    except Exception as e:
                        print(f"Error al registrar la venta: {e}")
                
                elif opcion_ventas == "2":
                    # Ver todas las ventas
                    menu_view.display_all_ventas()
                
                elif opcion_ventas == "3":
                    # Ver ventas por lotería
                    menu_view.display_ventas_por_loteria()
                
                elif opcion_ventas == "4":
                    # Ver total de ventas
                    menu_view.display_total_ventas()
                
                elif opcion_ventas == "5":
                    # Volver al menú principal
                    break
                
                else:
                    print("Opción no válida. Por favor intente de nuevo.")

        elif opcion == "6":
            menu_view.exit_message()
            break
        else:
            print("Opción no válida. Por favor intente de nuevo.")

if __name__ == "__main__":
    main()
