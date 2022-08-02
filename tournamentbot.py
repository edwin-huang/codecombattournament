team = -1
if hero.pos.x > 60:
    team = 1
towercoords = [
    {"x": 60 + team * 44 , "y": 50 + team * 35},
    {"x": 60 + team * 12 , "y": 50 + team * 45},
    {"x": 60 + team * 48 , "y": 50 + team * 4},
    {"x": 60 + team * 7 , "y": 50 + team * 7},
    {"x": 60 + team * 6 , "y": 50 + team * -40},
    {"x": 60 + team * -47 , "y": 50 + team * 14},
    {"x": 60 + team * -49 , "y": 50 + team * -40},
]
if team == 1:
    towercoords = [
        {"x": 60 + team * 44 , "y": 50 + team * 35},
        {"x": 60 + team * 48 , "y": 50 + team * 4},
        {"x": 60 + team * 12 , "y": 50 + team * 45},
        {"x": 60 + team * 7 , "y": 50 + team * 7},
        {"x": 60 + team * -47 , "y": 50 + team * 14},
        {"x": 60 + team * 6 , "y": 50 + team * -40},    
        {"x": 60 + team * -49 , "y": 50 + team * -40},
    ]

tosummon = ["archer", "archer", "soldier", "soldier", "artillery"]
summonind = 0

def posadd(pos1, pos2):
    return {"x": pos1.x + pos2.x, "y": pos1.y + pos2.y}

def posmult(pos, factor):
    return {"x": pos.x * factor, "y": pos.y * factor}

def posmag(pos, mag):
    possize = Math.hypot(pos.x, pos.y)
    return {"x": pos.x * mag/possize, "y": pos.y * mag/possize}

def distTo(pos1, pos2):
    return Math.hypot(pos1.x - pos2.x, pos1.y - pos2.y)

def vecto(mepos, tarpos, dist):
    possize = Math.hypot(mepos.x - tarpos.x, mepos.y - tarpos.y)
    return {"x": (tarpos.x - mepos.x) * dist/possize, "y": (tarpos.y - mepos.y) * dist/possize}

def goto(mepos, tarpos, dist):
    possize = Math.hypot(mepos.x - tarpos.x, mepos.y - tarpos.y)
    return posadd(mepos, {"x": (tarpos.x - mepos.x) * dist/possize, "y": (tarpos.y - mepos.y) * dist/possize})

def awayfrom(mepos, enpos, factor):
    return {"x": (factor + 1) * mepos.x - factor * enpos.x, "y": (factor + 1) * mepos.y - factor * enpos.y}

mid = {"x": 60, "y": 50}

arch = False
arti = False
harro = False
arro = False
artipos = False
artidist = 1000
arropos = False
arrodist = 1000
harropos = False
harrodist = 1000
archpos = False
archdist = 1000
ehero = False
eheropos = False
eherodist = 1000
scaryarrs = 0
enemyarts = 0
penemyarchs = 0
enemyarchs = 0
enemythrow = False
moveswitch = 1
ebould = -1

#0: opposing control #1: attacking #2: contested #3: nothing #4: going to #5: already there
towerstatus = [3, 3, 3, 3, 3, 3, 3]
towerdef = [-1, -1, -1, -1, -1, -1, -1]
archdef = []
soldblonk = []

friendstatus = []
points = hero.getControlPoints()
openspot = 10
openspots = 0

builttow = False

def getstats():
    enemies = hero.findEnemies()
    
    global arch, arti, harro, arro, ehero, artipos, artidist, arropos, arrodist, harropos, harrodist, archpos, archdist, eheropos, eherodist, penemyarchs, enemyarchs, enemyarts, scaryarrs, enemythrow, moveswitch, ebould, builttow
    
    arch = False
    arti = False
    harro = False
    arro = False
    ehero = False
    artipos = False
    artidist = 1000
    arropos = False
    arrodist = 1000
    harropos = False
    harrodist = 1000
    archpos = False
    archdist = 1000
    eheropos = False
    eherodist = 1000
    penemyarchs = enemyarchs
    enemyarchs = 0
    enemyarts = 0
    scaryarrs = 0
    builttow = False
    
    for en in enemies:
        if en.type == "goliath":
            ehero = en
            eheropos = en.pos
            eherodist = distTo(hero.pos, en.pos)
        elif en.type == "artillery":
            if distTo(hero.pos, en.pos) < artidist:
                arti = en
                artipos = en.pos
                artidist = distTo(hero.pos, en.pos)
            enemyarts += 1
        elif en.type == "arrow-tower":
            if distTo(en.pos, mid) < arrodist:
                arro = en
                arropos = en.pos
                arrodist = distTo(en.pos, mid)
            if distTo(hero.pos, en.pos) < harrodist:
                harro = en
                harropos = en.pos
                harrodist = distTo(mid, en.pos)
            if distTo(towercoords[1], en.pos) < 15 or distTo(towercoords[2], en.pos) < 15:
                scaryarrs += 1
        elif en.type == "archer":
            if distTo(hero.pos, en.pos) < archdist:
                arch = en
                archpos = en.pos
                archdist = distTo(hero.pos, en.pos)
            enemyarchs += 1
    
    penemythrow = enemythrow
    enemythrow = False
    ebould = -1
    for aa in hero.findEnemyMissiles():
        if aa.type == "boulder":
            ebould = aa
            enemythrow = True
    
    if not penemythrow and enemythrow:
        moveswitch *= -1
    
    for bob in hero.findByType("arrow-tower", hero.findFriends()):
        if distTo(bob.pos, towercoords[0]) > 10:
            builttow = True

def changefriendstatus():
    global towerstatus
    global towerdef
    global friendstatus
    global openspot
    global openspots
    
    allfriends = hero.built
    towerstatus = [3, 3, 3, 3, 3, 3, 0]
    towerdef =  [-1, -1, -1, -1, -1, -1, -1]
    openspot = 10
    openspots = 0
    
    #check scouts
    for i, friend in enumerate(allfriends):
        archdef[i] = -1
        
        if friend.health <= 0:
            friendstatus[i] = -1
            continue
        
        if friendstatus[i] != -1:
            towerstatus[friendstatus[i]] = 4
            towerdef[friendstatus[i]] = i
    
    for i, friend in enumerate(allfriends):
        if friend.health <= 13:
            soldblonk[i] = -1
            continue
        
        if friend.type == "soldier" and soldblonk[i] != -1:
            if allfriends[soldblonk[i]].health <= 0:
                soldblonk[i] = -1
                continue
            archdef[soldblonk[i]] = i
    
    #fill in towers by me
    for friend in hero.findFriends():
        for j, point in enumerate(points):
            if distTo(friend.pos, point.pos) < 10:
                towerstatus[j] = 5
    
    #fill in points by opponent
    for enemy in hero.findEnemies():
        for j, point in enumerate(points):
            if distTo(enemy.pos, point.pos) < 10:
                if towerstatus[j] == 4:
                    towerstatus[j] = 1
                elif towerstatus[j] == 5:
                    towerstatus[j] = 2
                else:
                    towerstatus[j] = 0
    
    #assign peoples
    for i, friend in enumerate(allfriends):
        if friend.health <= 0 or friendstatus[i] != -1 or friend.type != "archer":
            continue
        
        for j, point in enumerate(points):
            if towerstatus[j] == 3:
                friendstatus[i] = j
                towerstatus[j] = 4
                towerdef[j] = i
                break
    
    #check open spots
    for j, point in enumerate(points):
        if towerstatus[j] == 3:
            openspots = openspots + 1
            if openspot == 10:
                openspot = j
    
    #assign peoples
    for i, friend in enumerate(allfriends):
        if friend.health <= 13 or soldblonk[i] != -1 or friend.type != "soldier":
            continue
        
        for j, bob in enumerate(allfriends):
            if bob.type == "archer" and archdef[j] == -1 and bob.health > 0:
                soldblonk[i] = j
                archdef[j] = i
                break

def building():
    global builttow
    
    type = "arrow-tower"
    if ehero and (scaryarrs > 0 or enemyarts > 0 or distTo(eheropos, mid) > 30) and hero.time > 8:
        type = "artillery"
    if enemyarts < 1 and openspot < 3:
        type = "archer"
    sols = 0
    for bob in hero.findByType("soldier", hero.findFriends()):
        if bob.health > 13:
            sols += 1
    if len(hero.findByType("archer", hero.findFriends())) > sols and sols < 2:
        type = "soldier"
    if summonind < len(tosummon):
        type = tosummon[summonind]
    if hero.gold >= 125 and hero.time > 12:
        type = "archer"
    
    bb = False
    if hero.gold >= hero.costOf(type):
        if type == "soldier":
            hero.buildXY("soldier", hero.pos.x + team, hero.pos.y + team)
            bb = True
        if type == "archer":
            if openspot < 3 or (hero.time < 5 and openspot != 10):
                hero.buildXY("archer", goto(hero.pos, towercoords[openspot], 6.5).x, goto(hero.pos, towercoords[openspot], 6.5).y)
                bb = True
            elif not enemythrow:
                if hero.time < 6:
                    hero.buildXY("archer", goto(hero.pos, towercoords[3], 6.5).x, goto(hero.pos, towercoords[3], 6.5).y)
                else:
                    hero.buildXY("archer", goto(hero.pos, towercoords[0], 6.5).x, goto(hero.pos, towercoords[0], 6.5).y)
                bb = True
        elif type == "artillery":
            if hero.time < 5:
                hero.buildXY("artillery", hero.pos.x - 5 * team, hero.pos.y + 3 * team)
            else:
                hero.buildXY("artillery", hero.pos.x + 5 * team, hero.pos.y + 3 * team)
            bb = True
        elif type == "arrow-tower":
            bthing = 1
            if ehero and distTo({"x": hero.pos.x + 5 * bthing, "y": hero.pos.y - 5 * bthing}, ehero.pos) < distTo({"x": hero.pos.x - 5 * bthing, "y": hero.pos.y + 5 * bthing}, ehero.pos):
                bthing *= -1
            hero.buildXY("arrow-tower", hero.pos.x + 5 * bthing, hero.pos.y - 5 * bthing)
            if ehero and hero.distanceTo(ehero) < 9 and hero.isReady("hurl"):
                hero.hurl(ehero, awayfrom(ehero.pos, {"x": hero.pos.x + 5 * bthing, "y": hero.pos.y - 5 * bthing}, 10))
            builttow = True
            bb = True
        if bb:
            friendstatus.append(-1)
            archdef.append(-1)
            soldblonk.append(-1)
            summonind += 1

def armyAction():
    enemies = hero.findEnemies()
    friends = hero.built
    for i, friend in enumerate(friends):
        if friend.health <= 0:
            continue
        
        friendpos = friend.pos
        enemy = False
        nsold = False
        nart = False
        narr = False
        narch = False
        scaryarrdist = 1000
        for bob in enemies:
            bobdist = distTo(friendpos, bob.pos)
            if not enemy or bobdist < distTo(friendpos, enemy.pos):
                enemy = bob
            if bob.type == "soldier" and (not nsold or bobdist < distTo(friendpos, nsold.pos)):
                nsold = bob
            if bob.type == "archer" and (not narch or bobdist < distTo(friendpos, narch.pos)):
                narch = bob
            if bob.type == "artillery" and (not nart or bobdist < distTo(friendpos, nart.pos)):
                nart = bob
            if bob.type == "arrow-tower":
                if not narr or bobdist < distTo(friendpos, narr.pos):
                    narr = bob
                if (distTo(hero.pos, bob.pos) > bobdist or distTo(hero.pos, bob.pos) > 25) and bobdist < scaryarrdist:
                    scaryarr = bob
                    scaryarrdist = bobdist
        
        if friend.type == "soldier":
            if soldblonk[i] != -1:
                fenemysold = False
                fenemyarr = False
                fenemyarch = False
                for bob in hero.findByType("archer", hero.findEnemies()):
                    if not fenemyarch or distTo(friends[soldblonk[i]].pos, bob.pos) < distTo(friends[soldblonk[i]].pos, fenemyarch.pos):
                        fenemyarch = bob
                
                for bob in hero.findByType("soldier", hero.findEnemies()):
                    if not fenemysold or distTo(friends[soldblonk[i]].pos, bob.pos) < distTo(friends[soldblonk[i]].pos, fenemysold.pos):
                        fenemysold = bob
                
                for bob in hero.findByType("archer", hero.findEnemies()):
                    if not fenemyarr or distTo(friends[soldblonk[i]].pos, bob.pos) < distTo(friends[soldblonk[i]].pos, fenemyarr.pos):
                        fenemyarr = bob
                
                if fenemyarch:
                    hero.command(friend, "move", goto(friends[soldblonk[i]].pos, fenemyarch.pos, 3))
                elif fenemyarr:
                    hero.command(friend, "move", goto(friends[soldblonk[i]].pos, fenemyarr.pos, 3))
                elif fenemysold:
                    hero.command(friend, "move", goto(friends[soldblonk[i]].pos, fenemysold.pos, 3))
                else:
                    hero.command(friend, "move", friends[soldblonk[i]].pos)
            elif friend.health > 13:
                if openspot == 1 or openspot == 2:
                    hero.command(friend, "move", towercoords[openspot])
                else:
                    hero.command(friend, "move", towercoords[0])
        
        if friend.type == "archer":
            defpos = friendpos
            if friendstatus[i] != -1 and distTo(friendpos, towercoords[friendstatus[i]]) < 10:
                defpos = towercoords[friendstatus[i]]
            
            if ehero and friend.distanceTo(ehero) < 15:
                if friendstatus[i] == -1  or friendstatus[i] > 2:
                    hero.command(friend, "move", awayfrom(friendpos, eheropos, 10))
                else:
                    hero.command(friend, "move", towercoords[0])
            elif ehero and enemythrow and distTo(friendpos, {"x": ebould.targetPos.x, "y": ebould.targetPos.y}) < 15:
                if friendstatus[i] == -1  or friendstatus[i] > 2:
                    if distTo({"x": ebould.targetPos.x, "y": ebould.targetPos.y}, friendpos) == 0:
                        hero.command(friend, "move", towercoords[0])
                    elif moveswitch == 1:
                        hero.command(friend, "move", {"x": friendpos.x + vecto(friendpos, eheropos, 10).y, "y": friendpos.y - vecto(friendpos, eheropos, 10).x})
                    else:
                        hero.command(friend, "move", {"x": friendpos.x - vecto(friendpos, eheropos, 10).y, "y": friendpos.y + vecto(friendpos, eheropos, 10).x})
                else:
                    hero.command(friend, "move", towercoords[friendstatus[i]])
            elif scaryarr and distTo(friendpos, scaryarr.pos) < 34:
                if friendstatus[i] == -1  or friendstatus[i] > 2:
                    hero.command(friend, "move", awayfrom(friendpos, scaryarr.pos, 10))
                else:
                    hero.command(friend, "move", towercoords[friendstatus[i]])
            elif nart and distTo(defpos, nart.pos) < 28:
                hero.command(friend, "attack", nart)
            elif narch and distTo(defpos, narch.pos) < 28:
                hero.command(friend, "attack", narch)
            elif ehero and friend.distanceTo(ehero) < 20:
                if friendstatus[i] == -1  or friendstatus[i] > 2:
                    hero.command(friend, "move", awayfrom(friendpos, eheropos, 10))
                else:
                    hero.command(friend, "move", towercoords[friendstatus[i]])
            elif narr and distTo(defpos, narr.pos) < 28:
                hero.command(friend, "attack", narr)
            elif nsold and distTo(defpos, nsold.pos) < 10:
                hero.command(friend, "move", towercoords[0])
            elif friendstatus[i] == -1:
                if enemy and friend.distanceTo(enemy) < 28:
                    hero.command(friend, "attack", enemy)
                elif narch and friend.distanceTo(narch) < 35:
                    hero.command(friend, "move", narch.pos)
                elif towerstatus[4] < 2 and enemyarts == 0:
                    hero.command(friend, "move", towercoords[4])
                elif towerstatus[5] < 2 and enemyarts == 0:
                    hero.command(friend, "move", towercoords[5])
                elif len(hero.findFriends()) > 3 + 3 * len(enemies) and hero.time > 30:
                    hero.command(friend, "move", towercoords[6])
                else:
                    hero.command(friend, "move", towercoords[3])
            else:
                if nsold and distTo(friendpos, nsold.pos) < 28 and distTo(nsold.pos, towercoords[friendstatus[i]]) < 10:
                    hero.command(friend, "attack", nsold)
                else:
                    hero.command(friend, "move", towercoords[friendstatus[i]])
        
        if friend.type == "artillery":
            if nart and friend.distanceTo(nart) < 65:
                artillerypos = nart.pos
            elif narr and friend.distanceTo(narr) < 65:
                artillerypos = narr.pos
            elif nart:
                artillerypos = nart.pos
            elif narch and friend.distanceTo(narch) < 65 and hero.time > 10:
                artillerypos = narch.pos
            elif enemy and hero.time > 10:
                artillerypos = enemy.pos
            
            if artillerypos:
                if distTo(artillerypos, hero.pos) < 10:
                    hero.command(friend, "attackPos", awayfrom(artillerypos, hero.pos, 1))
                elif distTo(friendpos, artillerypos) > 65:
                    hero.command(friend, "move", artillerypos)
                else:
                    hero.command(friend, "attackPos", artillerypos)
            else:
                hero.command(friend, "attackPos", {"x": 60 - 28 * team, "y": 50 - 23 * team})
        
        if friend.type == "arrow-tower":
            if nart and distTo(friendpos, nart.pos) < 30:
                hero.command(friend, "attack", nart)
            elif narch and distTo(friendpos, narch.pos) < 30:
                hero.command(friend, "attack", narch)
            elif narr and distTo(friendpos, narr.pos) < 30:
                hero.command(friend, "attack", narr)

def heroAction():
    enemies = hero.findEnemies()
    nearestEnemy = hero.findNearest(enemies)
    
    if hero.isReady("stomp") and ((hero.time > 10 and (enemyarchs > penemyarchs or enemyarchs == 0)) or arch and distTo(hero.pos, arch.pos) < 15 or arti and distTo(hero.pos, arti.pos) < 15):
        hero.stomp()
    
    if artipos and artidist < 20:
        hero.attack(arti)
    elif harropos and harrodist < 30:
        hero.attack(harro)
    elif arropos and arrodist < 30:
        hero.attack(arro)
    elif distTo(hero.pos, mid) > 10 and hero.time > 2:
        hero.move(mid)
    elif archpos and archdist < 7:
        hero.attack(arch)
    elif ehero and hero.distanceTo(eheropos) < 10:
        hero.attack(ehero)
    elif nearestEnemy and hero.distanceTo(nearestEnemy) < 10:
        hero.attack(nearestEnemy)
    elif len(hero.findFriends()) > 3 + 3 * len(enemies) and hero.time > 30:
        hero.move(towercoords[6])
    elif summonind >= len(tosummon) or hero.gold < 25:
        hero.move(mid)
    
    if hero.isReady("stomp") and ((hero.time > 10 and (enemyarchs > penemyarchs or enemyarchs == 0)) or arch and distTo(hero.pos, arch.pos) < 15 or arti and distTo(hero.pos, arti.pos) < 15):
        hero.stomp()
    
    if hero.isReady("throw") and hero.time > 10:
        if artipos and artidist < hero.throwRange:
            hero.throwPos(goto(hero.pos, artipos, 25))
        elif arropos and arrodist < hero.throwRange:
            hero.throwPos(arropos)
        elif archpos and archdist < hero.throwRange:
            hero.throwPos(archpos)
        elif eheropos and eherodist < hero.throwRange:
            hero.throwPos(ehero.pos)
    
    if ehero and hero.findNearest(hero.findByType("arrow-tower", hero.findFriends())) and hero.gold < 50 and hero.isReady("hurl") and distTo(hero.findNearest(hero.findByType("arrow-tower", hero.findFriends())).pos, towercoords[0]) > 10:
        hero.hurl(ehero, awayfrom(ehero.pos, hero.findNearest(hero.findByType("arrow-tower", hero.findFriends())).pos, 10))

while True:
    getstats()
    changefriendstatus()
    building()
    armyAction()
    heroAction()

