Setup:
1. Copy the anim2shelf.py file to your Maya scripts folder.
2. Load the script from within Maya using the next 2 lines in Python:
import anim2shelf
anim2shelf.anim2Shelf()
3. Enjoy! :)

Usage:
1. Open the anim2shelf window.
2. Select controllers on your rig that you want to copy their animation to the current shelf.
3. Set the animation range that you'd like to copy - or just click the "Grab Range" button to set the rage from the timeslider.
4. Check Remember Namespace check box if you'd like the ability to paste current animation onto another instance of the same rig later
Leave it unchecked of you'll be pasting the animation onto the same rig (Removes unneeded code).
5. Press the "Create Button" button (It might take a while, please just bear with it).

What now?
A. If all went well, you now have a shelf button that recreates your animation for the same objects that you selected.
B. If you checked the "Rememder Namespace" option, you will be asked if you'd like to use the namespace of the first object of your current sleection 

* Note that pasting animation to another namespace will only work
if you copied animation of controllers from the same namespace and not multiple ones (Same rig not various different).
