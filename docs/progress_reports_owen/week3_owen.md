## Major Changes Completed

1. **Input Implementation & Migration**

   - Created `InputHandler` class in `src/view/input.py`.  
   - Encapsulates all keyboard → command mapping logic.  
   - Supported key mappings:  
     - ⬆️ `K_UP` → `"ROTATE"`  
     - ⬅️ `K_LEFT` → `"LEFT"`  
     - ➡️ `K_RIGHT` → `"RIGHT"`  
     - ⬇️ `K_DOWN` → `"DOWN"`  
     - ␣ `K_SPACE` → `"DROP"`  
     - ⏎ `K_RETURN` → `"START"`  
   - Integrated `InputHandler` into the `Game` class (`game.py`).  

2. **Import System**

   - Standardized import for input:  
     ```python
     from src.view.input import InputHandler
     ```

3. **Legacy Code Removal & Variable Updates**

   - Removed inline key handling from `game.py`.  
   - All keyboard logic now routed through `InputHandler`.  

4. **Function Updates**

   - **Intent Retrieval**  
     - Was:  
       ```python
       for event in pygame.event.get():
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_LEFT:
                   ...
       ```
     - Now:  
       ```python
       intents = self.input_handler.get_intents(events)
       ```

   - **Console Logging**  
     - Added logging of returned intents for verification:  
       ```python
       if intents:
           print("Intents:", intents)
       ```

## Current State

- **Functionality**: Keyboard inputs now mapped to commands, returned as intent lists.  
- **Code Quality**: Cleaner separation of concerns; `game.py` no longer has raw key handling.  
- **Imports**: Consistent with other modules (`from src.view...`).  
- **Verification**: Intents successfully logged in console during game loop.  
