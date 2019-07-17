'''
Provides a convenient representation of Jupyter's Slider widget and a manager to guarantee that all sliders always add to 1.0
(for weight sliders).
'''
import ipywidgets as widgets

__author__ = "Finn Frankis"
__copyright__ = "Copyright 2019, Crypticko"

MAX_VAL = 1.0
STEP = 0.01

'''
Wraps Jupyter's 'Slider' widget (stored as obj) with a slider description and a boolean keeping track of whether the slider was edited manually or programatically.
'''
class Slider:
   def __init__(self, description, obj):
      self.obj = obj
      self.editedManually = False
      self.description = description
      
   def getReading(self):
      return self.obj.value
   
   def setReading(self, newReading):
      self.obj.value = newReading
      
   '''
   Initializes the slider value given the initial value. This ensures that all
   sliders will start out with equal values.
   '''
   def initSliderValue(self, initVal):
      self.setReading(initVal)

# Manages any number of weight sliders, ensuring that they always add to 1.0 regardless of modification.
class SliderManager:
   '''
   Initializes the slider manager. editedFunction is the function to be triggered when a given slider is edited.
   All subsequent arguments are the sliders to be added to the manager.
   '''
   def __init__(self, editedFunction, slidersList):
      self.editedFunction = editedFunction
      self.slidersList = slidersList
      for slider in slidersList:
         slider.initSliderValue(MAX_VAL / len(slidersList))
         slider.obj.observe(self.sliderEdited, 'value')
        
   # Retrieves a given slider by its description.
   def getSlider(self, description):
      return [slider for slider in self.slidersList if slider.description == description][0]

   # Generates a box widget which displays any number of sliders adjacent to their description.
   def generateDisplayBox(self):
      leftBoxElements = [widgets.Label(slider.description) for slider in self.slidersList]
      rightBoxElements = [slider.obj for slider in self.slidersList]
      return widgets.HBox([widgets.VBox(leftBoxElements), widgets.VBox(rightBoxElements)])

   # Triggers when one of the sliders is edited.
   def sliderEdited(self, change):
      sliders = {slider.obj:slider for slider in self.slidersList}
      editedSlider = change.owner
      deltaVal = change.new - change.old
      diffPerSlider = deltaVal / (len(sliders) - 1)

      isEditingAnything = False
      for s, sliderProperties in sliders.items():
         isEditingAnything = isEditingAnything or sliderProperties.editedManually # determine whether any value in the sliders dictionary is True

      # If the user manually edited a different slider, then this function should exit early because it was triggered
      # by the programmatic editing of this slider. Prevents a recursive loop.
      if isEditingAnything:
         return False

      sliders[editedSlider].editedManually = True

      i = 0

      uneditedSliders = dict(sliders)
      uneditedSliders.pop(editedSlider)

      # Sort the sliders by the amount of distance they can move (the one with the greatest distance should be edited first).
      # If the edited slider was decreased, all the other sliders have to move up, so the one closest to 0.0 should come last.
      # If the edited slider was increased, all the other sliders have to move down, so the one closest to 1.0 should come last. 
      if deltaVal < 0:
         sortedSliders = sorted(uneditedSliders.items(), key = lambda kv: -kv[0].value)
      else:
         sortedSliders = sorted(uneditedSliders.items(), key = lambda kv: kv[0].value - MAX_VAL)

      for s, editing in sortedSliders:
         origVal = s.value
         s.value = max(0, s.value - diffPerSlider)

         # Only subtracts off the difference which was calculated in the slider (useful when the difference brings the
         # slider value to a number less than zero).
         deltaVal -= (origVal - s.value)
         if i != (len(sortedSliders) - 1): # avoid unnecessary division by zero on the last iteration (value will not be used again)
               diffPerSlider = deltaVal / (len(sortedSliders) - i - 1)
         i += 1
   
      # Reset that a value was edited manually to ensure other sliders can trigger this function.
      sliders[editedSlider].editedManually = False
      self.editedFunction()
