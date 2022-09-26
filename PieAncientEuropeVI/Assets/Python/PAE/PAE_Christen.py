# Christian features and events

# Imports
from CvPythonExtensions import (CyGlobalContext, CyInterface,
																CyTranslator, ColorTypes, isWorldWonderClass,
																isTeamWonderClass, isNationalWonderClass)
# import CvEventInterface
import CvUtil

# Defines
gc = CyGlobalContext()

# Globals
bChristentum = False


def init():
		global bChristentum
		bChristentum = gc.getGame().isReligionFounded(gc.getInfoTypeForString("RELIGION_CHRISTIANITY"))


def setHolyCity():
		global bChristentum
		# Stadt finden
		pCity = None
		iJudentum = gc.getInfoTypeForString("RELIGION_JUDAISM")
		# Prio1: Heilige Stadt des Judentums
		if gc.getGame().isReligionFounded(iJudentum):
				pCity = gc.getGame().getHolyCity(iJudentum)

		# Prio 2: Juedische Stadt
		if pCity is None:
				lCities = []
				iNumPlayers = gc.getMAX_PLAYERS()
				for i in range(iNumPlayers):
						loopPlayer = gc.getPlayer(i)
						if loopPlayer.isAlive():
								iNumCities = loopPlayer.getNumCities()
								for j in range(iNumCities):
										loopCity = loopPlayer.getCity(j)
										if loopCity is not None and not loopCity.isNone():
												if loopCity.isHasReligion(iJudentum):
														lCities.append(loopCity)

				if lCities:
						pCity = lCities[CvUtil.myRandom(len(lCities), "holy_jew")]

		# Prio3: Hauptstadt mit den meisten Sklaven (ink. Gladiatoren)
		# oder Prio 4: biggest capital city
		if pCity is None:
				# falls es nur Staedte ohne Sklaven gibt
				lCities = []
				# fuer den Vergleich mit Staedten mit Sklaven
				iSumSlaves = 0
				# biggest capital
				iPop = 0

				iNumPlayers = gc.getMAX_PLAYERS()
				for i in range(iNumPlayers):
						loopPlayer = gc.getPlayer(i)
						if loopPlayer.isAlive():
								loopCity = loopPlayer.getCapitalCity()
								if loopCity is not None and not loopCity.isNone():
										iSlaves = (loopCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GLADIATOR"))
															 + loopCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE"))
															 + loopCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE_FOOD"))
															 + loopCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE_PROD")))

										iCityPop = loopCity.getPopulation()
										if iSlaves == 0:
												if iCityPop > iPop:
														iPop = iCityPop
														lCities = []
														lCities.append(loopCity)
												elif iCityPop == iPop:
														lCities.append(loopCity)
										elif iSumSlaves < iSlaves:
												iSumSlaves = iSlaves
												pCity = loopCity

				if pCity is None:
						if lCities:
								pCity = lCities[CvUtil.myRandom(len(lCities), "holy")]

		# 1. Religion den Barbaren zukommen (sonst kommt Religionswahl bei Theologie)
		pBarbTeam = gc.getTeam(gc.getPlayer(gc.getBARBARIAN_PLAYER()).getTeam())
		pBarbTeam.setHasTech(gc.getInfoTypeForString("TECH_THEOLOGY"), True, gc.getBARBARIAN_PLAYER(), True, False)

		# 2. Heilige Stadt setzen
		if pCity is not None:
				gc.getGame().setHolyCity(gc.getInfoTypeForString("RELIGION_CHRISTIANITY"), pCity, True)
				bChristentum = True


def convertCity(pCity):
		iReligion = gc.getInfoTypeForString("RELIGION_CHRISTIANITY")
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)

		# nicht bei Judentum, Hindu, Buddh und Jain
		if (not pCity.isHasReligion(gc.getInfoTypeForString("RELIGION_JUDAISM"))
				and not pCity.isHasReligion(gc.getInfoTypeForString("RELIGION_HINDUISM"))
				and not pCity.isHasReligion(gc.getInfoTypeForString("RELIGION_BUDDHISM"))
						and not pCity.isHasReligion(gc.getInfoTypeForString("RELIGION_JAINISMUS"))):

				if pCity.isCapital():
						iChance = 40  # 2.5%
				elif pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_STADT")):
						if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_SKLAVENMARKT")):
								iChance = 30  # 3%
						else:
								iChance = 50  # 2%
				elif pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_SKLAVENMARKT")):
						iChance = 40  # 2.5%
				else:
						iChance = 75  # 1.5%

				# bei folgenden Civics Chance verringern
				if pPlayer.isCivic(gc.getInfoTypeForString("CIVIC_THEOCRACY")):
						iChance += 25
				if pPlayer.isCivic(gc.getInfoTypeForString("CIVIC_AMPHIKTIONIE")):
						iChance += 25

				if CvUtil.myRandom(iChance, "convertCity") == 1:
						pCity.setHasReligion(iReligion, 1, 1, 0)
						if pPlayer.isHuman():
								iRand = 1 + CvUtil.myRandom(3, "TXT_KEY_MESSAGE_HERESY_2CHRIST_")
								CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_HERESY_2CHRIST_"+str(iRand), (pCity.getName(), 0)),
																				 None, 2, "Art/Interface/Buttons/Actions/button_kreuz.dds", ColorTypes(11), pCity.getX(), pCity.getY(), True, True)


def removePagans(pCity):
		iReligion = gc.getInfoTypeForString("RELIGION_CHRISTIANITY")
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)

		# Kult
		lCorp = []
		iRange = gc.getNumCorporationInfos()
		for i in range(iRange):
				if pCity.isHasCorporation(i):
						lCorp.append(i)

		# Religion
		lReli = []
		iRange = gc.getNumReligionInfos()
		for i in range(iRange):
				if pCity.isHasReligion(i) and i != iReligion:
						lReli.append(i)

		# Kult oder Religion entfernen
		text = ""
		bUndoCorp = False
		if lCorp and lReli:
				if CvUtil.myRandom(2, "undoCorp") == 1:
						bUndoCorp = True

		# Kult
		if lCorp or bUndoCorp:
				iRand = CvUtil.myRandom(len(lCorp), "removePaganCult")
				iRange = gc.getNumBuildingInfos()
				for iBuildingLoop in range(iRange):
						if pCity.getNumBuilding(iBuildingLoop) > 0:
								pBuilding = gc.getBuildingInfo(iBuildingLoop)
								if pBuilding.getPrereqCorporation() == lCorp[iRand]:
										# Akademien (Corp7)
										if pBuilding.getType() not in [
														gc.getInfoTypeForString("BUILDING_ACADEMY_2"),
														gc.getInfoTypeForString("BUILDING_ACADEMY_3"),
														gc.getInfoTypeForString("BUILDING_ACADEMY_4")
										]:
												# Wunder sollen nicht betroffen werden
												iBuildingClass = pBuilding.getBuildingClassType()
												if not isWorldWonderClass(iBuildingClass) and not isTeamWonderClass(iBuildingClass) and not isNationalWonderClass(iBuildingClass):
														pCity.setNumRealBuilding(iBuildingLoop, 0)
				pCity.setHasCorporation(lCorp[iRand], 0, 0, 0)
				text = gc.getCorporationInfo(lCorp[iRand]).getText()

		# Religion
		elif lReli:
				iRand = CvUtil.myRandom(len(lReli), "removePaganReli")
				iRange = gc.getNumBuildingInfos()
				for iBuildingLoop in range(iRange):
						if pCity.isHasBuilding(iBuildingLoop):
								pBuilding = gc.getBuildingInfo(iBuildingLoop)
								if pBuilding.getPrereqReligion() == lReli[iRand]:
										# Holy City
										if pBuilding.getHolyCity() == -1:
												# Wunder sollen nicht betroffen werden
												iBuildingClass = pBuilding.getBuildingClassType()
												if not isWorldWonderClass(iBuildingClass) and not isTeamWonderClass(iBuildingClass) and not isNationalWonderClass(iBuildingClass):
														pCity.setNumRealBuilding(iBuildingLoop, 0)

				pCity.setHasReligion(lReli[iRand], 0, 0, 0)
				text = gc.getReligionInfo(lReli[iRand]).getText()

		# Meldung
		if pPlayer.isHuman() and text != "":
				iRand = 1 + CvUtil.myRandom(3, "TXT_KEY_MESSAGE_HERESY_CULTS_")
				CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_HERESY_CULTS_"+str(iRand), (text, pCity.getName())),
																 None, 2, "Art/Interface/Buttons/Actions/button_kreuz.dds", ColorTypes(11), pCity.getX(), pCity.getY(), True, True)
