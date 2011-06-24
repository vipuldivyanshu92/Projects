# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class AreatriggerInvolvedrelation(models.Model):
    id = models.IntegerField(primary_key=True)
    quest = models.IntegerField()
    class Meta:
        db_table = u'areatrigger_involvedrelation'

class AreatriggerTavern(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True)
    class Meta:
        db_table = u'areatrigger_tavern'

class AreatriggerTeleport(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True)
    required_level = models.IntegerField()
    required_item = models.IntegerField()
    required_item2 = models.IntegerField()
    heroic_key = models.IntegerField()
    heroic_key2 = models.IntegerField()
    required_quest_done = models.IntegerField()
    required_failed_text = models.TextField(blank=True)
    target_map = models.IntegerField()
    target_position_x = models.FloatField()
    target_position_y = models.FloatField()
    target_position_z = models.FloatField()
    target_orientation = models.FloatField()
    class Meta:
        db_table = u'areatrigger_teleport'

class BattlegroundTemplate(models.Model):
    id = models.IntegerField(primary_key=True)
    minplayersperteam = models.IntegerField()
    maxplayersperteam = models.IntegerField()
    minlvl = models.IntegerField()
    maxlvl = models.IntegerField()
    alliancestartloc = models.IntegerField()
    alliancestarto = models.FloatField()
    hordestartloc = models.IntegerField()
    hordestarto = models.FloatField()
    class Meta:
        db_table = u'battleground_template'

class BattlemasterEntry(models.Model):
    entry = models.IntegerField(primary_key=True)
    bg_template = models.IntegerField()
    class Meta:
        db_table = u'battlemaster_entry'

class Command(models.Model):
    name = models.CharField(max_length=150, primary_key=True)
    security = models.IntegerField()
    help = models.TextField(blank=True)
    class Meta:
        db_table = u'command'

class Creature(models.Model):
    guid = models.IntegerField(primary_key=True)
    id = models.IntegerField()
    map = models.IntegerField()
    spawnmask = models.IntegerField()
    modelid = models.IntegerField()
    equipment_id = models.IntegerField()
    position_x = models.FloatField()
    position_y = models.FloatField()
    position_z = models.FloatField()
    orientation = models.FloatField()
    spawntimesecs = models.IntegerField()
    spawndist = models.FloatField()
    currentwaypoint = models.IntegerField()
    curhealth = models.IntegerField()
    curmana = models.IntegerField()
    deathstate = models.IntegerField()
    movementtype = models.IntegerField()
    class Meta:
        db_table = u'creature'

class CreatureAddon(models.Model):
    guid = models.IntegerField(primary_key=True)
    mount = models.IntegerField()
    bytes0 = models.IntegerField()
    bytes1 = models.IntegerField()
    bytes2 = models.IntegerField()
    emote = models.IntegerField()
    moveflags = models.IntegerField()
    auras = models.TextField(blank=True)
    class Meta:
        db_table = u'creature_addon'

class CreatureEquipTemplate(models.Model):
    entry = models.IntegerField(primary_key=True)
    equipmodel1 = models.IntegerField()
    equipmodel2 = models.IntegerField()
    equipmodel3 = models.IntegerField()
    equipinfo1 = models.IntegerField()
    equipinfo2 = models.IntegerField()
    equipinfo3 = models.IntegerField()
    equipslot1 = models.IntegerField()
    equipslot2 = models.IntegerField()
    equipslot3 = models.IntegerField()
    class Meta:
        db_table = u'creature_equip_template'

class CreatureInvolvedrelation(models.Model):
    id = models.IntegerField(primary_key=True)
    quest = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'creature_involvedrelation'

class CreatureLootTemplate(models.Model):
    entry = models.IntegerField(primary_key=True)
    item = models.IntegerField(primary_key=True)
    chanceorquestchance = models.FloatField()
    groupid = models.IntegerField()
    mincountorref = models.IntegerField()
    maxcount = models.IntegerField()
    freeforall = models.IntegerField()
    lootcondition = models.IntegerField()
    condition_value1 = models.IntegerField()
    condition_value2 = models.IntegerField()
    class Meta:
        db_table = u'creature_loot_template'

class CreatureModelInfo(models.Model):
    modelid = models.IntegerField(primary_key=True)
    bounding_radius = models.FloatField()
    combat_reach = models.FloatField()
    gender = models.IntegerField()
    modelid_other_gender = models.IntegerField()
    class Meta:
        db_table = u'creature_model_info'

class CreatureMovement(models.Model):
    id = models.IntegerField(primary_key=True)
    point = models.IntegerField(primary_key=True)
    position_x = models.FloatField()
    position_y = models.FloatField()
    position_z = models.FloatField()
    waittime = models.IntegerField()
    text1 = models.TextField(blank=True)
    text2 = models.TextField(blank=True)
    text3 = models.TextField(blank=True)
    text4 = models.TextField(blank=True)
    text5 = models.TextField(blank=True)
    emote = models.IntegerField()
    spell = models.IntegerField()
    wpguid = models.IntegerField()
    orientation = models.FloatField()
    model1 = models.IntegerField()
    model2 = models.IntegerField()
    class Meta:
        db_table = u'creature_movement'

class CreatureOnkillReputation(models.Model):
    creature_id = models.IntegerField(primary_key=True)
    rewonkillrepfaction1 = models.IntegerField()
    rewonkillrepfaction2 = models.IntegerField()
    maxstanding1 = models.IntegerField()
    isteamaward1 = models.IntegerField()
    rewonkillrepvalue1 = models.IntegerField()
    maxstanding2 = models.IntegerField()
    isteamaward2 = models.IntegerField()
    rewonkillrepvalue2 = models.IntegerField()
    teamdependent = models.IntegerField()
    class Meta:
        db_table = u'creature_onkill_reputation'

class CreatureQuestrelation(models.Model):
    id = models.IntegerField(primary_key=True)
    quest = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'creature_questrelation'

class CreatureRespawn(models.Model):
    guid = models.IntegerField(primary_key=True)
    respawntime = models.IntegerField()
    instance = models.IntegerField()
    class Meta:
        db_table = u'creature_respawn'

class CreatureTemplate(models.Model):
    entry = models.IntegerField(primary_key=True)
    modelid_a = models.IntegerField()
    modelid_a2 = models.IntegerField()
    modelid_h = models.IntegerField()
    modelid_h2 = models.IntegerField()
    name = models.CharField(max_length=300)
    subname = models.CharField(max_length=300, blank=True)
    iconname = models.CharField(max_length=300, blank=True)
    minlevel = models.IntegerField()
    maxlevel = models.IntegerField()
    minhealth = models.IntegerField()
    maxhealth = models.IntegerField()
    minmana = models.IntegerField()
    maxmana = models.IntegerField()
    armor = models.IntegerField()
    faction_a = models.IntegerField()
    faction_h = models.IntegerField()
    npcflag = models.IntegerField()
    speed = models.FloatField()
    scale = models.FloatField()
    rank = models.IntegerField()
    mindmg = models.FloatField()
    maxdmg = models.FloatField()
    dmgschool = models.IntegerField()
    attackpower = models.IntegerField()
    baseattacktime = models.IntegerField()
    rangeattacktime = models.IntegerField()
    flags = models.IntegerField()
    dynamicflags = models.IntegerField()
    family = models.IntegerField()
    trainer_type = models.IntegerField()
    trainer_spell = models.IntegerField()
    class_field = models.IntegerField(db_column='class') # Field renamed because it was a Python reserved word.
    race = models.IntegerField()
    minrangedmg = models.FloatField()
    maxrangedmg = models.FloatField()
    rangedattackpower = models.IntegerField()
    type = models.IntegerField()
    civilian = models.IntegerField()
    flag1 = models.IntegerField()
    lootid = models.IntegerField()
    pickpocketloot = models.IntegerField()
    skinloot = models.IntegerField()
    resistance1 = models.IntegerField()
    resistance2 = models.IntegerField()
    resistance3 = models.IntegerField()
    resistance4 = models.IntegerField()
    resistance5 = models.IntegerField()
    resistance6 = models.IntegerField()
    spell1 = models.IntegerField()
    spell2 = models.IntegerField()
    spell3 = models.IntegerField()
    spell4 = models.IntegerField()
    mingold = models.IntegerField()
    maxgold = models.IntegerField()
    ainame = models.CharField(max_length=192)
    movementtype = models.IntegerField()
    inhabittype = models.IntegerField()
    racialleader = models.IntegerField()
    regenhealth = models.IntegerField()
    equipment_id = models.IntegerField()
    mechanic_immune_mask = models.IntegerField()
    scriptname = models.CharField(max_length=192)
    class Meta:
        db_table = u'creature_template'

class CreatureTemplateAddon(models.Model):
    entry = models.IntegerField(primary_key=True)
    mount = models.IntegerField()
    bytes0 = models.IntegerField()
    bytes1 = models.IntegerField()
    bytes2 = models.IntegerField()
    emote = models.IntegerField()
    moveflags = models.IntegerField()
    auras = models.TextField(blank=True)
    class Meta:
        db_table = u'creature_template_addon'

class DbVersion(models.Model):
    version = models.CharField(max_length=360, blank=True)
    class Meta:
        db_table = u'db_version'

class DisenchantLootTemplate(models.Model):
    entry = models.IntegerField(primary_key=True)
    item = models.IntegerField(primary_key=True)
    chanceorquestchance = models.FloatField()
    groupid = models.IntegerField()
    mincountorref = models.IntegerField()
    maxcount = models.IntegerField()
    freeforall = models.IntegerField()
    lootcondition = models.IntegerField()
    condition_value1 = models.IntegerField()
    condition_value2 = models.IntegerField()
    class Meta:
        db_table = u'disenchant_loot_template'

class EventScripts(models.Model):
    id = models.IntegerField()
    delay = models.IntegerField()
    command = models.IntegerField()
    datalong = models.IntegerField()
    datalong2 = models.IntegerField()
    datatext = models.TextField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    o = models.FloatField()
    class Meta:
        db_table = u'event_scripts'

class ExplorationBasexp(models.Model):
    level = models.IntegerField(primary_key=True)
    basexp = models.IntegerField()
    class Meta:
        db_table = u'exploration_basexp'

class FishingLootTemplate(models.Model):
    entry = models.IntegerField(primary_key=True)
    item = models.IntegerField(primary_key=True)
    chanceorquestchance = models.FloatField()
    groupid = models.IntegerField()
    mincountorref = models.IntegerField()
    maxcount = models.IntegerField()
    freeforall = models.IntegerField()
    lootcondition = models.IntegerField()
    condition_value1 = models.IntegerField()
    condition_value2 = models.IntegerField()
    class Meta:
        db_table = u'fishing_loot_template'

class GameEvent(models.Model):
    entry = models.IntegerField(primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    occurence = models.IntegerField()
    length = models.IntegerField()
    description = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'game_event'

class GameEventCreature(models.Model):
    guid = models.IntegerField(primary_key=True)
    event = models.IntegerField()
    class Meta:
        db_table = u'game_event_creature'

class GameEventCreatureQuest(models.Model):
    id = models.IntegerField(primary_key=True)
    quest = models.IntegerField(primary_key=True)
    event = models.IntegerField()
    class Meta:
        db_table = u'game_event_creature_quest'

class GameEventGameobject(models.Model):
    guid = models.IntegerField(primary_key=True)
    event = models.IntegerField()
    class Meta:
        db_table = u'game_event_gameobject'

class GameEventModelEquip(models.Model):
    guid = models.IntegerField(primary_key=True)
    modelid = models.IntegerField()
    equipment_id = models.IntegerField()
    event = models.IntegerField()
    class Meta:
        db_table = u'game_event_model_equip'

class GameGraveyardZone(models.Model):
    id = models.IntegerField(primary_key=True)
    ghost_zone = models.IntegerField(primary_key=True)
    faction = models.IntegerField()
    class Meta:
        db_table = u'game_graveyard_zone'

class GameTele(models.Model):
    id = models.IntegerField(primary_key=True)
    position_x = models.FloatField()
    position_y = models.FloatField()
    position_z = models.FloatField()
    orientation = models.FloatField()
    map = models.IntegerField()
    name = models.CharField(max_length=300)
    class Meta:
        db_table = u'game_tele'

class GameWeather(models.Model):
    zone = models.IntegerField(primary_key=True)
    spring_rain_chance = models.IntegerField()
    spring_snow_chance = models.IntegerField()
    spring_storm_chance = models.IntegerField()
    summer_rain_chance = models.IntegerField()
    summer_snow_chance = models.IntegerField()
    summer_storm_chance = models.IntegerField()
    fall_rain_chance = models.IntegerField()
    fall_snow_chance = models.IntegerField()
    fall_storm_chance = models.IntegerField()
    winter_rain_chance = models.IntegerField()
    winter_snow_chance = models.IntegerField()
    winter_storm_chance = models.IntegerField()
    class Meta:
        db_table = u'game_weather'

class Gameobject(models.Model):
    guid = models.IntegerField(primary_key=True)
    id = models.IntegerField()
    map = models.IntegerField()
    spawnmask = models.IntegerField()
    position_x = models.FloatField()
    position_y = models.FloatField()
    position_z = models.FloatField()
    orientation = models.FloatField()
    rotation0 = models.FloatField()
    rotation1 = models.FloatField()
    rotation2 = models.FloatField()
    rotation3 = models.FloatField()
    spawntimesecs = models.IntegerField()
    animprogress = models.IntegerField()
    state = models.IntegerField()
    class Meta:
        db_table = u'gameobject'

class GameobjectInvolvedrelation(models.Model):
    id = models.IntegerField(primary_key=True)
    quest = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'gameobject_involvedrelation'

class GameobjectLootTemplate(models.Model):
    entry = models.IntegerField(primary_key=True)
    item = models.IntegerField(primary_key=True)
    chanceorquestchance = models.FloatField()
    groupid = models.IntegerField()
    mincountorref = models.IntegerField()
    maxcount = models.IntegerField()
    freeforall = models.IntegerField()
    lootcondition = models.IntegerField()
    condition_value1 = models.IntegerField()
    condition_value2 = models.IntegerField()
    class Meta:
        db_table = u'gameobject_loot_template'

class GameobjectQuestrelation(models.Model):
    id = models.IntegerField(primary_key=True)
    quest = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'gameobject_questrelation'

class GameobjectRespawn(models.Model):
    guid = models.IntegerField(primary_key=True)
    respawntime = models.IntegerField()
    instance = models.IntegerField()
    class Meta:
        db_table = u'gameobject_respawn'

class GameobjectScripts(models.Model):
    id = models.IntegerField()
    delay = models.IntegerField()
    command = models.IntegerField()
    datalong = models.IntegerField()
    datalong2 = models.IntegerField()
    datatext = models.TextField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    o = models.FloatField()
    class Meta:
        db_table = u'gameobject_scripts'

class GameobjectTemplate(models.Model):
    entry = models.IntegerField(primary_key=True)
    type = models.IntegerField()
    displayid = models.IntegerField()
    name = models.CharField(max_length=300)
    castbarcaption = models.CharField(max_length=300)
    faction = models.IntegerField()
    flags = models.IntegerField()
    size = models.FloatField()
    data0 = models.IntegerField()
    data1 = models.IntegerField()
    data2 = models.IntegerField()
    data3 = models.IntegerField()
    data4 = models.IntegerField()
    data5 = models.IntegerField()
    data6 = models.IntegerField()
    data7 = models.IntegerField()
    data8 = models.IntegerField()
    data9 = models.IntegerField()
    data10 = models.IntegerField()
    data11 = models.IntegerField()
    data12 = models.IntegerField()
    data13 = models.IntegerField()
    data14 = models.IntegerField()
    data15 = models.IntegerField()
    data16 = models.IntegerField()
    data17 = models.IntegerField()
    data18 = models.IntegerField()
    data19 = models.IntegerField()
    data20 = models.IntegerField()
    data21 = models.IntegerField()
    data22 = models.IntegerField()
    data23 = models.IntegerField()
    scriptname = models.CharField(max_length=192)
    class Meta:
        db_table = u'gameobject_template'

class InstanceTemplate(models.Model):
    map = models.IntegerField(primary_key=True)
    parent = models.IntegerField()
    levelmin = models.IntegerField()
    levelmax = models.IntegerField()
    maxplayers = models.IntegerField()
    reset_delay = models.IntegerField()
    startlocx = models.FloatField(null=True, blank=True)
    startlocy = models.FloatField(null=True, blank=True)
    startlocz = models.FloatField(null=True, blank=True)
    startloco = models.FloatField(null=True, blank=True)
    script = models.CharField(max_length=384)
    class Meta:
        db_table = u'instance_template'

class ItemEnchantmentTemplate(models.Model):
    entry = models.IntegerField(primary_key=True)
    ench = models.IntegerField(primary_key=True)
    chance = models.FloatField()
    class Meta:
        db_table = u'item_enchantment_template'

class ItemLootTemplate(models.Model):
    entry = models.IntegerField(primary_key=True)
    item = models.IntegerField(primary_key=True)
    chanceorquestchance = models.FloatField()
    groupid = models.IntegerField()
    mincountorref = models.IntegerField()
    maxcount = models.IntegerField()
    freeforall = models.IntegerField()
    lootcondition = models.IntegerField()
    condition_value1 = models.IntegerField()
    condition_value2 = models.IntegerField()
    class Meta:
        db_table = u'item_loot_template'

class ItemTemplate(models.Model):
    entry = models.IntegerField(primary_key=True)
    class_field = models.IntegerField(db_column='class') # Field renamed because it was a Python reserved word.
    subclass = models.IntegerField()
    unk0 = models.IntegerField()
    name = models.CharField(max_length=765)
    displayid = models.IntegerField()
    quality = models.IntegerField()
    flags = models.IntegerField()
    buycount = models.IntegerField()
    buyprice = models.IntegerField()
    sellprice = models.IntegerField()
    inventorytype = models.IntegerField()
    allowableclass = models.IntegerField()
    allowablerace = models.IntegerField()
    itemlevel = models.IntegerField()
    requiredlevel = models.IntegerField()
    requiredskill = models.IntegerField()
    requiredskillrank = models.IntegerField()
    requiredspell = models.IntegerField()
    requiredhonorrank = models.IntegerField()
    requiredcityrank = models.IntegerField()
    requiredreputationfaction = models.IntegerField()
    requiredreputationrank = models.IntegerField()
    maxcount = models.IntegerField()
    stackable = models.IntegerField()
    containerslots = models.IntegerField()
    stat_type1 = models.IntegerField()
    stat_value1 = models.IntegerField()
    stat_type2 = models.IntegerField()
    stat_value2 = models.IntegerField()
    stat_type3 = models.IntegerField()
    stat_value3 = models.IntegerField()
    stat_type4 = models.IntegerField()
    stat_value4 = models.IntegerField()
    stat_type5 = models.IntegerField()
    stat_value5 = models.IntegerField()
    stat_type6 = models.IntegerField()
    stat_value6 = models.IntegerField()
    stat_type7 = models.IntegerField()
    stat_value7 = models.IntegerField()
    stat_type8 = models.IntegerField()
    stat_value8 = models.IntegerField()
    stat_type9 = models.IntegerField()
    stat_value9 = models.IntegerField()
    stat_type10 = models.IntegerField()
    stat_value10 = models.IntegerField()
    dmg_min1 = models.FloatField()
    dmg_max1 = models.FloatField()
    dmg_type1 = models.IntegerField()
    dmg_min2 = models.FloatField()
    dmg_max2 = models.FloatField()
    dmg_type2 = models.IntegerField()
    dmg_min3 = models.FloatField()
    dmg_max3 = models.FloatField()
    dmg_type3 = models.IntegerField()
    dmg_min4 = models.FloatField()
    dmg_max4 = models.FloatField()
    dmg_type4 = models.IntegerField()
    dmg_min5 = models.FloatField()
    dmg_max5 = models.FloatField()
    dmg_type5 = models.IntegerField()
    armor = models.IntegerField()
    holy_res = models.IntegerField()
    fire_res = models.IntegerField()
    nature_res = models.IntegerField()
    frost_res = models.IntegerField()
    shadow_res = models.IntegerField()
    arcane_res = models.IntegerField()
    delay = models.IntegerField()
    ammo_type = models.IntegerField()
    rangedmodrange = models.FloatField()
    spellid_1 = models.IntegerField()
    spelltrigger_1 = models.IntegerField()
    spellcharges_1 = models.IntegerField()
    spellppmrate_1 = models.FloatField()
    spellcooldown_1 = models.IntegerField()
    spellcategory_1 = models.IntegerField()
    spellcategorycooldown_1 = models.IntegerField()
    spellid_2 = models.IntegerField()
    spelltrigger_2 = models.IntegerField()
    spellcharges_2 = models.IntegerField()
    spellppmrate_2 = models.FloatField()
    spellcooldown_2 = models.IntegerField()
    spellcategory_2 = models.IntegerField()
    spellcategorycooldown_2 = models.IntegerField()
    spellid_3 = models.IntegerField()
    spelltrigger_3 = models.IntegerField()
    spellcharges_3 = models.IntegerField()
    spellppmrate_3 = models.FloatField()
    spellcooldown_3 = models.IntegerField()
    spellcategory_3 = models.IntegerField()
    spellcategorycooldown_3 = models.IntegerField()
    spellid_4 = models.IntegerField()
    spelltrigger_4 = models.IntegerField()
    spellcharges_4 = models.IntegerField()
    spellppmrate_4 = models.FloatField()
    spellcooldown_4 = models.IntegerField()
    spellcategory_4 = models.IntegerField()
    spellcategorycooldown_4 = models.IntegerField()
    spellid_5 = models.IntegerField()
    spelltrigger_5 = models.IntegerField()
    spellcharges_5 = models.IntegerField()
    spellppmrate_5 = models.FloatField()
    spellcooldown_5 = models.IntegerField()
    spellcategory_5 = models.IntegerField()
    spellcategorycooldown_5 = models.IntegerField()
    bonding = models.IntegerField()
    description = models.CharField(max_length=765)
    pagetext = models.IntegerField()
    languageid = models.IntegerField()
    pagematerial = models.IntegerField()
    startquest = models.IntegerField()
    lockid = models.IntegerField()
    material = models.IntegerField()
    sheath = models.IntegerField()
    randomproperty = models.IntegerField()
    randomsuffix = models.IntegerField()
    block = models.IntegerField()
    itemset = models.IntegerField()
    maxdurability = models.IntegerField()
    area = models.IntegerField()
    map = models.IntegerField()
    bagfamily = models.IntegerField()
    totemcategory = models.IntegerField()
    socketcolor_1 = models.IntegerField()
    socketcontent_1 = models.IntegerField()
    socketcolor_2 = models.IntegerField()
    socketcontent_2 = models.IntegerField()
    socketcolor_3 = models.IntegerField()
    socketcontent_3 = models.IntegerField()
    socketbonus = models.IntegerField()
    gemproperties = models.IntegerField()
    requireddisenchantskill = models.IntegerField()
    armordamagemodifier = models.FloatField()
    scriptname = models.CharField(max_length=192)
    disenchantid = models.IntegerField()
    foodtype = models.IntegerField()
    minmoneyloot = models.IntegerField()
    maxmoneyloot = models.IntegerField()
    duration = models.IntegerField()
    class Meta:
        db_table = u'item_template'

class LocalesCreature(models.Model):
    entry = models.IntegerField(primary_key=True)
    name_loc1 = models.CharField(max_length=300)
    name_loc2 = models.CharField(max_length=300)
    name_loc3 = models.CharField(max_length=300)
    name_loc4 = models.CharField(max_length=300)
    name_loc5 = models.CharField(max_length=300)
    name_loc6 = models.CharField(max_length=300)
    name_loc7 = models.CharField(max_length=300)
    subname_loc1 = models.CharField(max_length=300, blank=True)
    subname_loc2 = models.CharField(max_length=300, blank=True)
    subname_loc3 = models.CharField(max_length=300, blank=True)
    subname_loc4 = models.CharField(max_length=300, blank=True)
    subname_loc5 = models.CharField(max_length=300, blank=True)
    subname_loc6 = models.CharField(max_length=300, blank=True)
    subname_loc7 = models.CharField(max_length=300, blank=True)
    class Meta:
        db_table = u'locales_creature'

class LocalesGameobject(models.Model):
    entry = models.IntegerField(primary_key=True)
    name_loc1 = models.CharField(max_length=300)
    name_loc2 = models.CharField(max_length=300)
    name_loc3 = models.CharField(max_length=300)
    name_loc4 = models.CharField(max_length=300)
    name_loc5 = models.CharField(max_length=300)
    name_loc6 = models.CharField(max_length=300)
    name_loc7 = models.CharField(max_length=300)
    castbarcaption_loc1 = models.CharField(max_length=300)
    castbarcaption_loc2 = models.CharField(max_length=300)
    castbarcaption_loc3 = models.CharField(max_length=300)
    castbarcaption_loc4 = models.CharField(max_length=300)
    castbarcaption_loc5 = models.CharField(max_length=300)
    castbarcaption_loc6 = models.CharField(max_length=300)
    castbarcaption_loc7 = models.CharField(max_length=300)
    class Meta:
        db_table = u'locales_gameobject'

class LocalesItem(models.Model):
    entry = models.IntegerField(primary_key=True)
    name_loc1 = models.CharField(max_length=300)
    name_loc2 = models.CharField(max_length=300)
    name_loc3 = models.CharField(max_length=300)
    name_loc4 = models.CharField(max_length=300)
    name_loc5 = models.CharField(max_length=300)
    name_loc6 = models.CharField(max_length=300)
    name_loc7 = models.CharField(max_length=300)
    description_loc1 = models.CharField(max_length=765, blank=True)
    description_loc2 = models.CharField(max_length=765, blank=True)
    description_loc3 = models.CharField(max_length=765, blank=True)
    description_loc4 = models.CharField(max_length=765, blank=True)
    description_loc5 = models.CharField(max_length=765, blank=True)
    description_loc6 = models.CharField(max_length=765, blank=True)
    description_loc7 = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'locales_item'

class LocalesNpcText(models.Model):
    entry = models.IntegerField(primary_key=True)
    text0_0_loc1 = models.TextField(blank=True)
    text0_0_loc2 = models.TextField(blank=True)
    text0_0_loc3 = models.TextField(blank=True)
    text0_0_loc4 = models.TextField(blank=True)
    text0_0_loc5 = models.TextField(blank=True)
    text0_0_loc6 = models.TextField(blank=True)
    text0_0_loc7 = models.TextField(blank=True)
    text0_1_loc1 = models.TextField(blank=True)
    text0_1_loc2 = models.TextField(blank=True)
    text0_1_loc3 = models.TextField(blank=True)
    text0_1_loc4 = models.TextField(blank=True)
    text0_1_loc5 = models.TextField(blank=True)
    text0_1_loc6 = models.TextField(blank=True)
    text0_1_loc7 = models.TextField(blank=True)
    text1_0_loc1 = models.TextField(blank=True)
    text1_0_loc2 = models.TextField(blank=True)
    text1_0_loc3 = models.TextField(blank=True)
    text1_0_loc4 = models.TextField(blank=True)
    text1_0_loc5 = models.TextField(blank=True)
    text1_0_loc6 = models.TextField(blank=True)
    text1_0_loc7 = models.TextField(blank=True)
    text1_1_loc1 = models.TextField(blank=True)
    text1_1_loc2 = models.TextField(blank=True)
    text1_1_loc3 = models.TextField(blank=True)
    text1_1_loc4 = models.TextField(blank=True)
    text1_1_loc5 = models.TextField(blank=True)
    text1_1_loc6 = models.TextField(blank=True)
    text1_1_loc7 = models.TextField(blank=True)
    text2_0_loc1 = models.TextField(blank=True)
    text2_0_loc2 = models.TextField(blank=True)
    text2_0_loc3 = models.TextField(blank=True)
    text2_0_loc4 = models.TextField(blank=True)
    text2_0_loc5 = models.TextField(blank=True)
    text2_0_loc6 = models.TextField(blank=True)
    text2_0_loc7 = models.TextField(blank=True)
    text2_1_loc1 = models.TextField(blank=True)
    text2_1_loc2 = models.TextField(blank=True)
    text2_1_loc3 = models.TextField(blank=True)
    text2_1_loc4 = models.TextField(blank=True)
    text2_1_loc5 = models.TextField(blank=True)
    text2_1_loc6 = models.TextField(blank=True)
    text2_1_loc7 = models.TextField(blank=True)
    text3_0_loc1 = models.TextField(blank=True)
    text3_0_loc2 = models.TextField(blank=True)
    text3_0_loc3 = models.TextField(blank=True)
    text3_0_loc4 = models.TextField(blank=True)
    text3_0_loc5 = models.TextField(blank=True)
    text3_0_loc6 = models.TextField(blank=True)
    text3_0_loc7 = models.TextField(blank=True)
    text3_1_loc1 = models.TextField(blank=True)
    text3_1_loc2 = models.TextField(blank=True)
    text3_1_loc3 = models.TextField(blank=True)
    text3_1_loc4 = models.TextField(blank=True)
    text3_1_loc5 = models.TextField(blank=True)
    text3_1_loc6 = models.TextField(blank=True)
    text3_1_loc7 = models.TextField(blank=True)
    text4_0_loc1 = models.TextField(blank=True)
    text4_0_loc2 = models.TextField(blank=True)
    text4_0_loc3 = models.TextField(blank=True)
    text4_0_loc4 = models.TextField(blank=True)
    text4_0_loc5 = models.TextField(blank=True)
    text4_0_loc6 = models.TextField(blank=True)
    text4_0_loc7 = models.TextField(blank=True)
    text4_1_loc1 = models.TextField(blank=True)
    text4_1_loc2 = models.TextField(blank=True)
    text4_1_loc3 = models.TextField(blank=True)
    text4_1_loc4 = models.TextField(blank=True)
    text4_1_loc5 = models.TextField(blank=True)
    text4_1_loc6 = models.TextField(blank=True)
    text4_1_loc7 = models.TextField(blank=True)
    text5_0_loc1 = models.TextField(blank=True)
    text5_0_loc2 = models.TextField(blank=True)
    text5_0_loc3 = models.TextField(blank=True)
    text5_0_loc4 = models.TextField(blank=True)
    text5_0_loc5 = models.TextField(blank=True)
    text5_0_loc6 = models.TextField(blank=True)
    text5_0_loc7 = models.TextField(blank=True)
    text5_1_loc1 = models.TextField(blank=True)
    text5_1_loc2 = models.TextField(blank=True)
    text5_1_loc3 = models.TextField(blank=True)
    text5_1_loc4 = models.TextField(blank=True)
    text5_1_loc5 = models.TextField(blank=True)
    text5_1_loc6 = models.TextField(blank=True)
    text5_1_loc7 = models.TextField(blank=True)
    text6_0_loc1 = models.TextField(blank=True)
    text6_0_loc2 = models.TextField(blank=True)
    text6_0_loc3 = models.TextField(blank=True)
    text6_0_loc4 = models.TextField(blank=True)
    text6_0_loc5 = models.TextField(blank=True)
    text6_0_loc6 = models.TextField(blank=True)
    text6_0_loc7 = models.TextField(blank=True)
    text6_1_loc1 = models.TextField(blank=True)
    text6_1_loc2 = models.TextField(blank=True)
    text6_1_loc3 = models.TextField(blank=True)
    text6_1_loc4 = models.TextField(blank=True)
    text6_1_loc5 = models.TextField(blank=True)
    text6_1_loc6 = models.TextField(blank=True)
    text6_1_loc7 = models.TextField(blank=True)
    text7_0_loc1 = models.TextField(blank=True)
    text7_0_loc2 = models.TextField(blank=True)
    text7_0_loc3 = models.TextField(blank=True)
    text7_0_loc4 = models.TextField(blank=True)
    text7_0_loc5 = models.TextField(blank=True)
    text7_0_loc6 = models.TextField(blank=True)
    text7_0_loc7 = models.TextField(blank=True)
    text7_1_loc1 = models.TextField(blank=True)
    text7_1_loc2 = models.TextField(blank=True)
    text7_1_loc3 = models.TextField(blank=True)
    text7_1_loc4 = models.TextField(blank=True)
    text7_1_loc5 = models.TextField(blank=True)
    text7_1_loc6 = models.TextField(blank=True)
    text7_1_loc7 = models.TextField(blank=True)
    class Meta:
        db_table = u'locales_npc_text'

class LocalesPageText(models.Model):
    entry = models.IntegerField(primary_key=True)
    text_loc1 = models.TextField(blank=True)
    text_loc2 = models.TextField(blank=True)
    text_loc3 = models.TextField(blank=True)
    text_loc4 = models.TextField(blank=True)
    text_loc5 = models.TextField(blank=True)
    text_loc6 = models.TextField(blank=True)
    text_loc7 = models.TextField(blank=True)
    class Meta:
        db_table = u'locales_page_text'

class LocalesQuest(models.Model):
    entry = models.IntegerField(primary_key=True)
    title_loc1 = models.TextField(blank=True)
    title_loc2 = models.TextField(blank=True)
    title_loc3 = models.TextField(blank=True)
    title_loc4 = models.TextField(blank=True)
    title_loc5 = models.TextField(blank=True)
    title_loc6 = models.TextField(blank=True)
    title_loc7 = models.TextField(blank=True)
    details_loc1 = models.TextField(blank=True)
    details_loc2 = models.TextField(blank=True)
    details_loc3 = models.TextField(blank=True)
    details_loc4 = models.TextField(blank=True)
    details_loc5 = models.TextField(blank=True)
    details_loc6 = models.TextField(blank=True)
    details_loc7 = models.TextField(blank=True)
    objectives_loc1 = models.TextField(blank=True)
    objectives_loc2 = models.TextField(blank=True)
    objectives_loc3 = models.TextField(blank=True)
    objectives_loc4 = models.TextField(blank=True)
    objectives_loc5 = models.TextField(blank=True)
    objectives_loc6 = models.TextField(blank=True)
    objectives_loc7 = models.TextField(blank=True)
    offerrewardtext_loc1 = models.TextField(blank=True)
    offerrewardtext_loc2 = models.TextField(blank=True)
    offerrewardtext_loc3 = models.TextField(blank=True)
    offerrewardtext_loc4 = models.TextField(blank=True)
    offerrewardtext_loc5 = models.TextField(blank=True)
    offerrewardtext_loc6 = models.TextField(blank=True)
    offerrewardtext_loc7 = models.TextField(blank=True)
    requestitemstext_loc1 = models.TextField(blank=True)
    requestitemstext_loc2 = models.TextField(blank=True)
    requestitemstext_loc3 = models.TextField(blank=True)
    requestitemstext_loc4 = models.TextField(blank=True)
    requestitemstext_loc5 = models.TextField(blank=True)
    requestitemstext_loc6 = models.TextField(blank=True)
    requestitemstext_loc7 = models.TextField(blank=True)
    endtext_loc1 = models.TextField(blank=True)
    endtext_loc2 = models.TextField(blank=True)
    endtext_loc3 = models.TextField(blank=True)
    endtext_loc4 = models.TextField(blank=True)
    endtext_loc5 = models.TextField(blank=True)
    endtext_loc6 = models.TextField(blank=True)
    endtext_loc7 = models.TextField(blank=True)
    objectivetext1_loc1 = models.TextField(blank=True)
    objectivetext1_loc2 = models.TextField(blank=True)
    objectivetext1_loc3 = models.TextField(blank=True)
    objectivetext1_loc4 = models.TextField(blank=True)
    objectivetext1_loc5 = models.TextField(blank=True)
    objectivetext1_loc6 = models.TextField(blank=True)
    objectivetext1_loc7 = models.TextField(blank=True)
    objectivetext2_loc1 = models.TextField(blank=True)
    objectivetext2_loc2 = models.TextField(blank=True)
    objectivetext2_loc3 = models.TextField(blank=True)
    objectivetext2_loc4 = models.TextField(blank=True)
    objectivetext2_loc5 = models.TextField(blank=True)
    objectivetext2_loc6 = models.TextField(blank=True)
    objectivetext2_loc7 = models.TextField(blank=True)
    objectivetext3_loc1 = models.TextField(blank=True)
    objectivetext3_loc2 = models.TextField(blank=True)
    objectivetext3_loc3 = models.TextField(blank=True)
    objectivetext3_loc4 = models.TextField(blank=True)
    objectivetext3_loc5 = models.TextField(blank=True)
    objectivetext3_loc6 = models.TextField(blank=True)
    objectivetext3_loc7 = models.TextField(blank=True)
    objectivetext4_loc1 = models.TextField(blank=True)
    objectivetext4_loc2 = models.TextField(blank=True)
    objectivetext4_loc3 = models.TextField(blank=True)
    objectivetext4_loc4 = models.TextField(blank=True)
    objectivetext4_loc5 = models.TextField(blank=True)
    objectivetext4_loc6 = models.TextField(blank=True)
    objectivetext4_loc7 = models.TextField(blank=True)
    class Meta:
        db_table = u'locales_quest'

class MangosString(models.Model):
    entry = models.IntegerField(primary_key=True)
    content_default = models.TextField()
    content_loc1 = models.TextField(blank=True)
    content_loc2 = models.TextField(blank=True)
    content_loc3 = models.TextField(blank=True)
    content_loc4 = models.TextField(blank=True)
    content_loc5 = models.TextField(blank=True)
    content_loc6 = models.TextField(blank=True)
    content_loc7 = models.TextField(blank=True)
    class Meta:
        db_table = u'mangos_string'

class NpcGossip(models.Model):
    npc_guid = models.IntegerField(primary_key=True)
    textid = models.IntegerField()
    class Meta:
        db_table = u'npc_gossip'

class NpcGossipTextid(models.Model):
    zoneid = models.IntegerField()
    action = models.IntegerField()
    textid = models.IntegerField()
    class Meta:
        db_table = u'npc_gossip_textid'

class NpcOption(models.Model):
    id = models.IntegerField(primary_key=True)
    gossip_id = models.IntegerField()
    npcflag = models.IntegerField()
    icon = models.IntegerField()
    action = models.IntegerField()
    option_text = models.TextField(blank=True)
    class Meta:
        db_table = u'npc_option'

class NpcText(models.Model):
    id = models.IntegerField()
    text0_0 = models.TextField(blank=True)
    text0_1 = models.TextField(blank=True)
    lang0 = models.IntegerField()
    prob0 = models.FloatField()
    em0_0 = models.IntegerField()
    em0_1 = models.IntegerField()
    em0_2 = models.IntegerField()
    em0_3 = models.IntegerField()
    em0_4 = models.IntegerField()
    em0_5 = models.IntegerField()
    text1_0 = models.TextField(blank=True)
    text1_1 = models.TextField(blank=True)
    lang1 = models.IntegerField()
    prob1 = models.FloatField()
    em1_0 = models.IntegerField()
    em1_1 = models.IntegerField()
    em1_2 = models.IntegerField()
    em1_3 = models.IntegerField()
    em1_4 = models.IntegerField()
    em1_5 = models.IntegerField()
    text2_0 = models.TextField(blank=True)
    text2_1 = models.TextField(blank=True)
    lang2 = models.IntegerField()
    prob2 = models.FloatField()
    em2_0 = models.IntegerField()
    em2_1 = models.IntegerField()
    em2_2 = models.IntegerField()
    em2_3 = models.IntegerField()
    em2_4 = models.IntegerField()
    em2_5 = models.IntegerField()
    text3_0 = models.TextField(blank=True)
    text3_1 = models.TextField(blank=True)
    lang3 = models.IntegerField()
    prob3 = models.FloatField()
    em3_0 = models.IntegerField()
    em3_1 = models.IntegerField()
    em3_2 = models.IntegerField()
    em3_3 = models.IntegerField()
    em3_4 = models.IntegerField()
    em3_5 = models.IntegerField()
    text4_0 = models.TextField(blank=True)
    text4_1 = models.TextField(blank=True)
    lang4 = models.IntegerField()
    prob4 = models.FloatField()
    em4_0 = models.IntegerField()
    em4_1 = models.IntegerField()
    em4_2 = models.IntegerField()
    em4_3 = models.IntegerField()
    em4_4 = models.IntegerField()
    em4_5 = models.IntegerField()
    text5_0 = models.TextField(blank=True)
    text5_1 = models.TextField(blank=True)
    lang5 = models.IntegerField()
    prob5 = models.FloatField()
    em5_0 = models.IntegerField()
    em5_1 = models.IntegerField()
    em5_2 = models.IntegerField()
    em5_3 = models.IntegerField()
    em5_4 = models.IntegerField()
    em5_5 = models.IntegerField()
    text6_0 = models.TextField(blank=True)
    text6_1 = models.TextField(blank=True)
    lang6 = models.IntegerField()
    prob6 = models.FloatField()
    em6_0 = models.IntegerField()
    em6_1 = models.IntegerField()
    em6_2 = models.IntegerField()
    em6_3 = models.IntegerField()
    em6_4 = models.IntegerField()
    em6_5 = models.IntegerField()
    text7_0 = models.TextField(blank=True)
    text7_1 = models.TextField(blank=True)
    lang7 = models.IntegerField()
    prob7 = models.FloatField()
    em7_0 = models.IntegerField()
    em7_1 = models.IntegerField()
    em7_2 = models.IntegerField()
    em7_3 = models.IntegerField()
    em7_4 = models.IntegerField()
    em7_5 = models.IntegerField()
    class Meta:
        db_table = u'npc_text'

class NpcTrainer(models.Model):
    entry = models.IntegerField(unique=True)
    spell = models.IntegerField(unique=True)
    spellcost = models.IntegerField()
    reqskill = models.IntegerField()
    reqskillvalue = models.IntegerField()
    reqlevel = models.IntegerField()
    class Meta:
        db_table = u'npc_trainer'

class NpcVendor(models.Model):
    entry = models.IntegerField(primary_key=True)
    item = models.IntegerField(primary_key=True)
    maxcount = models.IntegerField()
    incrtime = models.IntegerField()
    extendedcost = models.IntegerField()
    class Meta:
        db_table = u'npc_vendor'

class PageText(models.Model):
    entry = models.IntegerField(primary_key=True)
    text = models.TextField()
    next_page = models.IntegerField()
    class Meta:
        db_table = u'page_text'

class PetLevelstats(models.Model):
    creature_entry = models.IntegerField(primary_key=True)
    level = models.IntegerField(primary_key=True)
    hp = models.IntegerField()
    mana = models.IntegerField()
    armor = models.IntegerField()
    str = models.IntegerField()
    agi = models.IntegerField()
    sta = models.IntegerField()
    inte = models.IntegerField()
    spi = models.IntegerField()
    class Meta:
        db_table = u'pet_levelstats'

class PetNameGeneration(models.Model):
    id = models.IntegerField(primary_key=True)
    word = models.TextField()
    entry = models.IntegerField()
    half = models.IntegerField()
    class Meta:
        db_table = u'pet_name_generation'

class PetcreateinfoSpell(models.Model):
    entry = models.IntegerField(primary_key=True)
    spell1 = models.IntegerField()
    spell2 = models.IntegerField()
    spell3 = models.IntegerField()
    spell4 = models.IntegerField()
    familypassive = models.IntegerField()
    class Meta:
        db_table = u'petcreateinfo_spell'

class PickpocketingLootTemplate(models.Model):
    entry = models.IntegerField(primary_key=True)
    item = models.IntegerField(primary_key=True)
    chanceorquestchance = models.FloatField()
    groupid = models.IntegerField()
    mincountorref = models.IntegerField()
    maxcount = models.IntegerField()
    freeforall = models.IntegerField()
    lootcondition = models.IntegerField()
    condition_value1 = models.IntegerField()
    condition_value2 = models.IntegerField()
    class Meta:
        db_table = u'pickpocketing_loot_template'

class PlayerClasslevelstats(models.Model):
    class_field = models.IntegerField(primary_key=True, db_column='class') # Field renamed because it was a Python reserved word.
    level = models.IntegerField(primary_key=True)
    basehp = models.IntegerField()
    basemana = models.IntegerField()
    class Meta:
        db_table = u'player_classlevelstats'

class PlayerLevelstats(models.Model):
    race = models.IntegerField(primary_key=True)
    class_field = models.IntegerField(primary_key=True, db_column='class') # Field renamed because it was a Python reserved word.
    level = models.IntegerField(primary_key=True)
    str = models.IntegerField()
    agi = models.IntegerField()
    sta = models.IntegerField()
    inte = models.IntegerField()
    spi = models.IntegerField()
    class Meta:
        db_table = u'player_levelstats'

class Playercreateinfo(models.Model):
    race = models.IntegerField(primary_key=True)
    class_field = models.IntegerField(primary_key=True, db_column='class') # Field renamed because it was a Python reserved word.
    map = models.IntegerField()
    zone = models.IntegerField()
    position_x = models.FloatField()
    position_y = models.FloatField()
    position_z = models.FloatField()
    class Meta:
        db_table = u'playercreateinfo'

class PlayercreateinfoAction(models.Model):
    race = models.IntegerField()
    class_field = models.IntegerField(db_column='class') # Field renamed because it was a Python reserved word.
    button = models.IntegerField()
    action = models.IntegerField()
    type = models.IntegerField()
    misc = models.IntegerField()
    class Meta:
        db_table = u'playercreateinfo_action'

class PlayercreateinfoItem(models.Model):
    race = models.IntegerField()
    class_field = models.IntegerField(db_column='class') # Field renamed because it was a Python reserved word.
    itemid = models.IntegerField()
    amount = models.IntegerField()
    class Meta:
        db_table = u'playercreateinfo_item'

class PlayercreateinfoSkill(models.Model):
    race = models.IntegerField(primary_key=True)
    class_field = models.IntegerField(primary_key=True, db_column='class') # Field renamed because it was a Python reserved word.
    skill = models.IntegerField()
    note = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'playercreateinfo_skill'

class PlayercreateinfoSpell(models.Model):
    race = models.IntegerField(primary_key=True)
    class_field = models.IntegerField(primary_key=True, db_column='class') # Field renamed because it was a Python reserved word.
    spell = models.IntegerField()
    note = models.CharField(max_length=765, blank=True)
    active = models.IntegerField()
    class Meta:
        db_table = u'playercreateinfo_spell'

class ProspectingLootTemplate(models.Model):
    entry = models.IntegerField(primary_key=True)
    item = models.IntegerField(primary_key=True)
    chanceorquestchance = models.FloatField()
    groupid = models.IntegerField()
    mincountorref = models.IntegerField()
    maxcount = models.IntegerField()
    freeforall = models.IntegerField()
    lootcondition = models.IntegerField()
    condition_value1 = models.IntegerField()
    condition_value2 = models.IntegerField()
    class Meta:
        db_table = u'prospecting_loot_template'

class QuestEndScripts(models.Model):
    id = models.IntegerField()
    delay = models.IntegerField()
    command = models.IntegerField()
    datalong = models.IntegerField()
    datalong2 = models.IntegerField()
    datatext = models.TextField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    o = models.FloatField()
    class Meta:
        db_table = u'quest_end_scripts'

class QuestStartScripts(models.Model):
    id = models.IntegerField()
    delay = models.IntegerField()
    command = models.IntegerField()
    datalong = models.IntegerField()
    datalong2 = models.IntegerField()
    datatext = models.TextField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    o = models.FloatField()
    class Meta:
        db_table = u'quest_start_scripts'

class QuestTemplate(models.Model):
    entry = models.IntegerField(primary_key=True)
    zoneorsort = models.IntegerField()
    skillorclass = models.IntegerField()
    minlevel = models.IntegerField()
    questlevel = models.IntegerField()
    type = models.IntegerField()
    requiredraces = models.IntegerField()
    requiredskillvalue = models.IntegerField()
    repobjectivefaction = models.IntegerField()
    repobjectivevalue = models.IntegerField()
    requiredminrepfaction = models.IntegerField()
    requiredminrepvalue = models.IntegerField()
    requiredmaxrepfaction = models.IntegerField()
    requiredmaxrepvalue = models.IntegerField()
    suggestedplayers = models.IntegerField()
    limittime = models.IntegerField()
    questflags = models.IntegerField()
    specialflags = models.IntegerField()
    chartitleid = models.IntegerField()
    prevquestid = models.IntegerField()
    nextquestid = models.IntegerField()
    exclusivegroup = models.IntegerField()
    nextquestinchain = models.IntegerField()
    srcitemid = models.IntegerField()
    srcitemcount = models.IntegerField()
    srcspell = models.IntegerField()
    title = models.TextField(blank=True)
    details = models.TextField(blank=True)
    objectives = models.TextField(blank=True)
    offerrewardtext = models.TextField(blank=True)
    requestitemstext = models.TextField(blank=True)
    endtext = models.TextField(blank=True)
    objectivetext1 = models.TextField(blank=True)
    objectivetext2 = models.TextField(blank=True)
    objectivetext3 = models.TextField(blank=True)
    objectivetext4 = models.TextField(blank=True)
    reqitemid1 = models.IntegerField()
    reqitemid2 = models.IntegerField()
    reqitemid3 = models.IntegerField()
    reqitemid4 = models.IntegerField()
    reqitemcount1 = models.IntegerField()
    reqitemcount2 = models.IntegerField()
    reqitemcount3 = models.IntegerField()
    reqitemcount4 = models.IntegerField()
    reqsourceid1 = models.IntegerField()
    reqsourceid2 = models.IntegerField()
    reqsourceid3 = models.IntegerField()
    reqsourceid4 = models.IntegerField()
    reqsourcecount1 = models.IntegerField()
    reqsourcecount2 = models.IntegerField()
    reqsourcecount3 = models.IntegerField()
    reqsourcecount4 = models.IntegerField()
    reqsourceref1 = models.IntegerField()
    reqsourceref2 = models.IntegerField()
    reqsourceref3 = models.IntegerField()
    reqsourceref4 = models.IntegerField()
    reqcreatureorgoid1 = models.IntegerField()
    reqcreatureorgoid2 = models.IntegerField()
    reqcreatureorgoid3 = models.IntegerField()
    reqcreatureorgoid4 = models.IntegerField()
    reqcreatureorgocount1 = models.IntegerField()
    reqcreatureorgocount2 = models.IntegerField()
    reqcreatureorgocount3 = models.IntegerField()
    reqcreatureorgocount4 = models.IntegerField()
    reqspellcast1 = models.IntegerField()
    reqspellcast2 = models.IntegerField()
    reqspellcast3 = models.IntegerField()
    reqspellcast4 = models.IntegerField()
    rewchoiceitemid1 = models.IntegerField()
    rewchoiceitemid2 = models.IntegerField()
    rewchoiceitemid3 = models.IntegerField()
    rewchoiceitemid4 = models.IntegerField()
    rewchoiceitemid5 = models.IntegerField()
    rewchoiceitemid6 = models.IntegerField()
    rewchoiceitemcount1 = models.IntegerField()
    rewchoiceitemcount2 = models.IntegerField()
    rewchoiceitemcount3 = models.IntegerField()
    rewchoiceitemcount4 = models.IntegerField()
    rewchoiceitemcount5 = models.IntegerField()
    rewchoiceitemcount6 = models.IntegerField()
    rewitemid1 = models.IntegerField()
    rewitemid2 = models.IntegerField()
    rewitemid3 = models.IntegerField()
    rewitemid4 = models.IntegerField()
    rewitemcount1 = models.IntegerField()
    rewitemcount2 = models.IntegerField()
    rewitemcount3 = models.IntegerField()
    rewitemcount4 = models.IntegerField()
    rewrepfaction1 = models.IntegerField()
    rewrepfaction2 = models.IntegerField()
    rewrepfaction3 = models.IntegerField()
    rewrepfaction4 = models.IntegerField()
    rewrepfaction5 = models.IntegerField()
    rewrepvalue1 = models.IntegerField()
    rewrepvalue2 = models.IntegerField()
    rewrepvalue3 = models.IntegerField()
    rewrepvalue4 = models.IntegerField()
    rewrepvalue5 = models.IntegerField()
    reworreqmoney = models.IntegerField()
    rewmoneymaxlevel = models.IntegerField()
    rewspell = models.IntegerField()
    rewspellcast = models.IntegerField()
    pointmapid = models.IntegerField()
    pointx = models.FloatField()
    pointy = models.FloatField()
    pointopt = models.IntegerField()
    detailsemote1 = models.IntegerField()
    detailsemote2 = models.IntegerField()
    detailsemote3 = models.IntegerField()
    detailsemote4 = models.IntegerField()
    incompleteemote = models.IntegerField()
    completeemote = models.IntegerField()
    offerrewardemote1 = models.IntegerField()
    offerrewardemote2 = models.IntegerField()
    offerrewardemote3 = models.IntegerField()
    offerrewardemote4 = models.IntegerField()
    startscript = models.IntegerField()
    completescript = models.IntegerField()
    class Meta:
        db_table = u'quest_template'

class ReservedName(models.Model):
    name = models.CharField(max_length=36, primary_key=True)
    class Meta:
        db_table = u'reserved_name'

class SkillDiscoveryTemplate(models.Model):
    spellid = models.IntegerField()
    reqspell = models.IntegerField()
    chance = models.FloatField()
    class Meta:
        db_table = u'skill_discovery_template'

class SkillExtraItemTemplate(models.Model):
    spellid = models.IntegerField()
    requiredspecialization = models.IntegerField()
    additionalcreatechance = models.FloatField()
    additionalmaxnum = models.IntegerField()
    class Meta:
        db_table = u'skill_extra_item_template'

class SkillFishingBaseLevel(models.Model):
    entry = models.IntegerField(primary_key=True)
    skill = models.IntegerField()
    class Meta:
        db_table = u'skill_fishing_base_level'

class SkinningLootTemplate(models.Model):
    entry = models.IntegerField(primary_key=True)
    item = models.IntegerField(primary_key=True)
    chanceorquestchance = models.FloatField()
    groupid = models.IntegerField()
    mincountorref = models.IntegerField()
    maxcount = models.IntegerField()
    freeforall = models.IntegerField()
    lootcondition = models.IntegerField()
    condition_value1 = models.IntegerField()
    condition_value2 = models.IntegerField()
    class Meta:
        db_table = u'skinning_loot_template'

class SpellAffect(models.Model):
    entry = models.IntegerField(primary_key=True)
    effectid = models.IntegerField()
    spellfamilymask = models.IntegerField()
    class Meta:
        db_table = u'spell_affect'

class SpellChain(models.Model):
    spell_id = models.IntegerField(primary_key=True)
    prev_spell = models.IntegerField()
    first_spell = models.IntegerField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'spell_chain'

class SpellElixir(models.Model):
    entry = models.IntegerField(primary_key=True)
    mask = models.IntegerField()
    class Meta:
        db_table = u'spell_elixir'

class SpellLearnSkill(models.Model):
    entry = models.IntegerField(unique=True)
    skillid = models.IntegerField()
    value = models.IntegerField()
    maxvalue = models.IntegerField()
    class Meta:
        db_table = u'spell_learn_skill'

class SpellLearnSpell(models.Model):
    entry = models.IntegerField(primary_key=True)
    spellid = models.IntegerField()
    class Meta:
        db_table = u'spell_learn_spell'

class SpellProcEvent(models.Model):
    entry = models.IntegerField(primary_key=True)
    schoolmask = models.IntegerField()
    category = models.IntegerField()
    skillid = models.IntegerField()
    spellfamilyname = models.IntegerField()
    spellfamilymask = models.IntegerField()
    procflags = models.IntegerField()
    ppmrate = models.FloatField()
    class Meta:
        db_table = u'spell_proc_event'

class SpellScriptTarget(models.Model):
    entry = models.IntegerField(unique=True)
    type = models.IntegerField(unique=True)
    targetentry = models.IntegerField()
    class Meta:
        db_table = u'spell_script_target'

class SpellScripts(models.Model):
    id = models.IntegerField()
    delay = models.IntegerField()
    command = models.IntegerField()
    datalong = models.IntegerField()
    datalong2 = models.IntegerField()
    datatext = models.TextField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    o = models.FloatField()
    class Meta:
        db_table = u'spell_scripts'

class SpellTeleport(models.Model):
    id = models.IntegerField(primary_key=True)
    target_map = models.IntegerField()
    target_position_x = models.FloatField()
    target_position_y = models.FloatField()
    target_position_z = models.FloatField()
    target_orientation = models.FloatField()
    class Meta:
        db_table = u'spell_teleport'

class SpellThreat(models.Model):
    entry = models.IntegerField(primary_key=True)
    threat = models.IntegerField()
    class Meta:
        db_table = u'spell_threat'

class Transports(models.Model):
    entry = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True)
    period = models.IntegerField()
    class Meta:
        db_table = u'transports'

class Uptime(models.Model):
    starttime = models.IntegerField(primary_key=True)
    startstring = models.CharField(max_length=192)
    uptime = models.IntegerField()
    maxplayers = models.IntegerField()
    class Meta:
        db_table = u'uptime'

