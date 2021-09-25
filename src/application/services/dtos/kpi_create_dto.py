import math
import re

from application.services.dtos.exceptions.exceptions import InvalidEquationError, LongitudeEquationError, LongitudeNameError, LongitudeUnitsError

class KpiCreateDto():

  def __init__(self, name: str, equation: str, units: str) -> None:
    if(len(name) <= 50):
      self.name = name
    else:
      raise LongitudeNameError

    if(len(equation) <= 100):

      hasX = re.search("(?<![a-zA-Z])[x](?![a-zA-Z])", equation)
      if(hasX == None): raise InvalidEquationError

      alfabethicElements = re.findall("[a-zA-Z]+", equation)
      for alfabethicElement in alfabethicElements:
        print(f'>> Element: {alfabethicElement}')
        isVariable = re.search("^[x]$", alfabethicElement)
        isConstant = re.search("^[A-Z]$", alfabethicElement)
        isMathFunction = getattr(math, alfabethicElement, None)

        if(isMathFunction):
          isPi = re.search("^[pi]$", alfabethicElement)
          isE = re.search("^[e]$", alfabethicElement)
          isMethod = None if re.search(f"{alfabethicElement}(?![(])", equation) != None else True

          if(isPi == None and isE == None and isMethod == None): raise InvalidEquationError

        if(isVariable == None and isConstant == None and isMathFunction == None): raise InvalidEquationError

      try:
        eval(equation)
      except SyntaxError:
        raise InvalidEquationError
      except NameError:
        pass

      self.equation = equation
    else:
      raise LongitudeEquationError

    if(len(units) <= 20):
      self.units = units
    else:
      raise LongitudeUnitsError

  def get_id(self) -> str:
    return self.id

  def get_name(self) -> str:
    return self.name

  def get_equation(self) -> str:
    return self.equation

  def get_units(self) -> str:
    return self.units
