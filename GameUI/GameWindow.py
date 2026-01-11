# from pyglet import text, app, clock
# from pyglet.window import key, mouse, Window


# gameWindow = Window(1280, 720, "Rue the Day", resizable=True)
# keyPressed = None
# # gameWindow.push_handlers(window.event.WindowEventLogger())

# label = text.Label("Hello Pyglet",
#                     font_name="Times New Roman", font_size=28,
#                     x=gameWindow.width/2, y=gameWindow.height/2,
#                     anchor_x="center", anchor_y="center")

# gameWindow.set_minimum_size(400, 300)


# @gameWindow.event
# def on_mouse_press(x, y, button, modifiers):
#     if button == mouse.LEFT:
#         print("left")
#     elif button == mouse.RIGHT:
#         print("right")

# @gameWindow.event
# def on_key_press(symbol, modifiers):
#     global keyPressed

#     match symbol:
#         case key._0: keyPressed = 0
#         case key._1: keyPressed = 1
#         case key._2: keyPressed = 2
#         case key._3: keyPressed = 3
#         case key._4: keyPressed = 4
#         case key._5: keyPressed = 5
#         case key._6: keyPressed = 6
#         case key._7: keyPressed = 7
#         case key._8: keyPressed = 8
#         case key._9: keyPressed = 9


# # def update(dt):
# #     global keyPressed
# #     if keyPressed:
# #         keyPressed = None

# # clock.schedule_interval(update, 1)

# @gameWindow.event
# def on_draw():
#     gameWindow.clear()
#     label.draw()


# app.run()