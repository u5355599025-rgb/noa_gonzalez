
import math
import random
import time
import turtle

WORLD_SIZE = 120
MAX_STEPS = 40

TERRAINS = {
    "desierto": {"energy": -5},
    "hielo": {"energy": -3},
    "bosque": {"energy": -4},
    "ruinas": {"energy": -2}
}

WORLD_OBJECTS = [
    "tormenta",
    "crater",
    "portal",
    "base_abandonada",
    "mineral_raro",
    "zona_radioactiva"
]

RANDOM_EVENTS = [
    "meteoritos",
    "piratas",
    "senal_alienigena",
    "calma",
    "sobrecarga"
]


class Rover:
    def __init__(self, name, x, y, angle, energy, oxygen, hull):
        self.name = name
        self.x = x
        self.y = y
        self.angle = angle
        self.energy = energy
        self.oxygen = oxygen
        self.hull = hull
        self.points = 0
        self.inventory = []
        self.history = []


def ask_int(message, default):
    value = input(message).strip()
    try:
        return int(value)
    except ValueError:
        print(f"[Sistema] Valor inválido. Usando {default}")
        return default


def intro():
    print("=" * 65)
    print("     🌌 GALACTIC ODYSSEY - SIMULADOR DE EXPEDICIÓN 🌌")
    print("=" * 65)
    print("Eres el comandante de un rover enviado a un planeta")
    print("desconocido lleno de ruinas, tormentas y tecnología alien.")
    print()


def setup_turtle():
    screen = turtle.Screen()
    screen.title("Mapa de Galactic Odyssey")
    screen.bgcolor("black")
    screen.setup(width=900, height=900)

    border = turtle.Turtle()
    border.speed(0)
    border.color("white")
    border.hideturtle()

    border.penup()
    border.goto(-WORLD_SIZE * 2, -WORLD_SIZE * 2)
    border.pendown()

    for _ in range(4):
        border.forward(WORLD_SIZE * 4)
        border.left(90)

    rover_pen = turtle.Turtle()
    rover_pen.shape("turtle")
    rover_pen.color("cyan")
    rover_pen.speed(0)
    rover_pen.pensize(2)

    return screen, rover_pen


def draw_special_points():
    deco = turtle.Turtle()
    deco.hideturtle()
    deco.speed(0)

    points = [
        (-80, 60, "yellow"),
        (50, 40, "red"),
        (70, -70, "green"),
        (-40, -90, "orange")
    ]

    for px, py, color in points:
        deco.penup()
        deco.goto(px * 2, py * 2)
        deco.dot(14, color)


def get_terrain():
    return random.choice(list(TERRAINS.keys()))


def apply_terrain(rover, terrain):
    rover.energy += TERRAINS[terrain]["energy"]


def world_object_effect(rover, obj):
    text = ""

    if obj == "tormenta":
        rover.energy -= 15
        rover.hull -= 5
        text = "⚠ Una tormenta electromagnética golpea el rover."

    elif obj == "crater":
        rover.x -= 5
        rover.y -= 5
        rover.energy -= 5
        text = "🕳 El rover cae parcialmente en un cráter."

    elif obj == "portal":
        rover.x = random.randint(-60, 60)
        rover.y = random.randint(-60, 60)
        rover.points += 15
        text = "🌀 Un portal alienígena teletransporta el rover."

    elif obj == "base_abandonada":
        rover.energy += 20
        rover.oxygen += 10
        rover.inventory.append("pieza tecnológica")
        text = "🏚 El rover encuentra una base abandonada."

    elif obj == "mineral_raro":
        rover.points += 25
        rover.inventory.append("mineral raro")
        text = "💎 Mineral raro recolectado."

    elif obj == "zona_radioactiva":
        rover.hull -= 12
        rover.energy -= 8
        text = "☢ Zona radioactiva detectada."

    return text


def random_event_effect(rover, event):
    text = ""

    if event == "meteoritos":
        rover.hull -= 10
        text = "☄ Lluvia de meteoritos impacta el rover."

    elif event == "piratas":
        lost = random.randint(5, 20)
        rover.points -= lost
        text = f"🏴 Piratas espaciales roban {lost} puntos."

    elif event == "senal_alienigena":
        rover.angle = (rover.angle + 90) % 360
        rover.points += 10
        text = "📡 Señal alienígena cambia la dirección."

    elif event == "sobrecarga":
        rover.energy += 15
        text = "⚡ El reactor entra en sobrecarga positiva."

    else:
        text = "🌠 El viaje continúa sin incidentes."

    return text


def move_rover(rover):
    distance = random.randint(6, 18)

    old_x = rover.x
    old_y = rover.y

    rover.x += round(math.cos(math.radians(rover.angle)) * distance)
    rover.y += round(math.sin(math.radians(rover.angle)) * distance)

    rover.energy -= random.randint(4, 9)
    rover.oxygen -= random.randint(2, 5)

    if rover.x > WORLD_SIZE:
        rover.x = WORLD_SIZE
        rover.energy -= 5

    if rover.x < -WORLD_SIZE:
        rover.x = -WORLD_SIZE
        rover.energy -= 5

    if rover.y > WORLD_SIZE:
        rover.y = WORLD_SIZE
        rover.energy -= 5

    if rover.y < -WORLD_SIZE:
        rover.y = -WORLD_SIZE
        rover.energy -= 5

    return old_x, old_y, distance


def print_hud(rover):
    print(f"🔋 Energía: {rover.energy}")
    print(f"🫁 Oxígeno: {rover.oxygen}")
    print(f"🛡 Integridad: {rover.hull}")
    print(f"🏆 Puntos: {rover.points}")
    print(f"🎒 Inventario: {rover.inventory}")


def final_report(rover, reason, steps):
    print("\n" + "=" * 60)
    print("                 INFORME FINAL")
    print("=" * 60)

    print(f"🚀 Rover: {rover.name}")
    print(f"📍 Posición final: ({rover.x}, {rover.y})")
    print(f"👣 Pasos realizados: {steps}")
    print(f"🔋 Energía restante: {rover.energy}")
    print(f"🫁 Oxígeno restante: {rover.oxygen}")
    print(f"🛡 Integridad final: {rover.hull}")
    print(f"🏆 Puntuación total: {rover.points}")
    print(f"🎒 Inventario final: {rover.inventory}")
    print(f"📜 Historial importante:")
    for item in rover.history[-10:]:
        print(f"   - {item}")

    print(f"\n❌ Motivo de finalización: {reason}")

    if rover.points >= 120:
        print("🌟 RESULTADO: ÉXITO LEGENDARIO")
    elif rover.points >= 60:
        print("✅ RESULTADO: MISIÓN EXITOSA")
    elif rover.points >= 20:
        print("⚠ RESULTADO: ÉXITO PARCIAL")
    else:
        print("💀 RESULTADO: FRACASO")

    print("=" * 60)


def play():
    intro()

    name = input("Nombre del rover: ").strip() or "Astra-X"

    x = ask_int("Posición inicial X: ", 0)
    y = ask_int("Posición inicial Y: ", 0)
    angle = ask_int("Ángulo inicial (0-359): ", 0)
    energy = ask_int("Energía inicial: ", 100)
    oxygen = ask_int("Oxígeno inicial: ", 80)
    hull = ask_int("Integridad del casco: ", 100)

    rover = Rover(name, x, y, angle, energy, oxygen, hull)

    target_x = random.randint(-90, 90)
    target_y = random.randint(-90, 90)

    print("\n🎯 OBJETIVO PRINCIPAL")
    print(f"Llegar cerca de ({target_x}, {target_y})")
    print(f"Límites del mundo: {-WORLD_SIZE} a {WORLD_SIZE}")
    print(f"Máximo de pasos: {MAX_STEPS}")

    screen, rover_pen = setup_turtle()
    draw_special_points()

    rover_pen.penup()
    rover_pen.goto(rover.x * 2, rover.y * 2)
    rover_pen.pendown()

    end_reason = "desconocido"

    for step in range(1, MAX_STEPS + 1):

        print("\n" + "-" * 60)
        print(f"🛰 PASO {step}")
        print("-" * 60)

        old_x, old_y, distance = move_rover(rover)

        terrain = get_terrain()
        apply_terrain(rover, terrain)

        obj = random.choice(WORLD_OBJECTS)
        obj_text = world_object_effect(rover, obj)

        event = random.choice(RANDOM_EVENTS)
        event_text = random_event_effect(rover, event)

        rover_pen.goto(rover.x * 2, rover.y * 2)
        rover_pen.dot(5)

        print(f"➡ Movimiento: {distance} unidades")
        print(f"📍 Antes: ({old_x}, {old_y})")
        print(f"📍 Después: ({rover.x}, {rover.y})")
        print(f"🌍 Terreno: {terrain}")
        print(obj_text)
        print(event_text)

        print_hud(rover)

        rover.history.append(obj_text)
        rover.history.append(event_text)

        if rover.energy <= 0:
            end_reason = "Sin energía"
            break

        if rover.oxygen <= 0:
            end_reason = "Sin oxígeno"
            break

        if rover.hull <= 0:
            end_reason = "Casco destruido"
            break

        if abs(rover.x - target_x) <= 8 and abs(rover.y - target_y) <= 8:
            rover.points += 50
            end_reason = "Objetivo alcanzado"
            break

        time.sleep(0.2)

    rover_pen.color("red")
    rover_pen.dot(14)

    final_report(rover, end_reason, step)

    print("\nCierra la ventana turtle para continuar.")
    screen.mainloop()


def main():
    while True:
        play()

        again = input("\n¿Iniciar nueva expedición? (s/n): ").lower()

        if again != "s":
            print("👋 Cerrando Galactic Odyssey...")
            break


if __name__ == "__main__":
    main()
