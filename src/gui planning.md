1. Rename the screen to window
2. A *Screen* will be my toplevel object
    - Only 1 of these will ever render at a time
3. The screen will be populated with widgets ( [] )

# Widget List
- Canvas
    - Per pixel drawing
    - Should have prebuilt primitive shapes
- Label
    - Textbox with optional background
    - Will only render on on_enter
    - Non-wrapped text
- Message
    - Wrapped text (longer sentences)
- Scrollbar
    - Translates all other widgets in its parent Frame
- Frame
    - Has its own widgets array
    - Can have a single scrollbar
    - Can also have a background colour
- Button
    - Callback
