import re
import random
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RULES = [
    # Greetings
    (r'\b(hi|hello|hey|howdy|sup|yo)\b',
     [r"Yo! NBA HQ is open 🏀 Ask me anything — players, teams, rules, records. I got you.",
      r"Hey! You've come to the right place for hoops knowledge. What do you want to know?",
      r"What's good! Pull up a seat and let's talk basketball. What's on your mind?"]),

    (r'\bgood\s+(morning|afternoon|evening|night)\b',
     [r"Good \1! You know what makes a \1 better? Talking about the NBA. Go ahead, ask me something.",
      r"Good \1! Whether the games are on or not, the knowledge never sleeps. What do you want to know?"]),

    (r'\bhow\s+are\s+you\b|\bhow\'?s\s+it\s+going\b',
     [r"I'm locked in and ready to drop buckets of NBA knowledge. What do you want to know?",
      r"Running at full speed, no turnovers. Ask me anything about basketball!"]),

    # Players
    (r'\b(lebron(\s+james)?|king\s+james)\b',
     [r"Oh you want to talk about \1? Strap in. 4 championships with 3 different teams, 4 Finals MVPs, 4 regular season MVPs, and in 2023 he walked past Kareem to become the all-time leading scorer with 40,000+ points. At year 20 he was still dropping 30-point games. Love him or hate him, there's no denying it — the man is an all-time freak of nature.",
      r"\1 came into the league at 18 with the weight of an entire city on his shoulders and somehow exceeded every expectation. 4 rings, all-time scoring record, and he did it across four decades of play. The 'King' nickname isn't ego — it's just accurate."]),

    (r'\b(michael\s+jordan|mj|air\s+jordan)\b',
     [r"You asked about \1 — buckle up. 6 championships. 6 Finals MVPs. 6 and 0 in the Finals. Never lost a championship series. Averaged 30.1 points per game for his career — still the highest ever. Oh and he did it all while being one of the best defenders on the floor every single night. The man didn't just win, he made winning look personal.",
      r"\1 is the reason 'GOAT' became a sports term. 10 scoring titles, 5 MVPs, 6 rings, and a Finals record that reads like a cheat code. The only debate about MJ is whether his floor was 'greatest ever' or 'greatest ever by a wide margin'."]),

    (r'\b(steph(en)?\s+curry)\b',
     [r"\1 broke basketball. That's not an exaggeration — he genuinely changed what the sport looks like at every level. Before Steph, shooting from 30 feet was a desperation heave. Now it's a strategy. 4 championships, 402 three-pointers in a single season, and the only unanimous MVP in NBA history. Oh, and he won a title without Kevin Durant just to prove a point.",
      r"You want to talk about \1? The man shoots from the logo and the defense just has to respect it. 4 rings, the all-time three-point record, and he redefined what a point guard can do. Defenders lose sleep over him."]),

    (r'\b(kobe(\s+bryant)?|black\s+mamba)\b',
     [r"\1 didn't play basketball — he hunted. 5 championships, 81 points in a single game against Toronto in 2006 (second-highest ever, and he did it in three quarters), 18 All-Star appearances, and a work ethic so legendary that 'Mamba Mentality' became a philosophy people actually live by. He made 4am workouts famous.",
      r"Ask anyone who watched \1 play and they'll tell you the same thing: he simply refused to lose. 5 rings with the Lakers, 81-point game, and a competitive fire that made even his teammates uncomfortable. One of a kind, truly."]),

    (r'\b(shaq(uille)?\s+o\'?neal|shaquille)\b',
     [r"\1 was not a basketball player. He was a natural disaster that happened to enjoy basketball. 7'1\", 325 lbs, and somehow still faster than most guards. 4 championships, 3-time Finals MVP, and he broke two shot-clock backboards in his career just by existing near them. Opposing teams literally had to invent a defensive strategy — 'Hack-a-Shaq' — just to survive him.",
      r"There has never been anyone like \1 and there probably never will be. When he was locked in, he was simply unguardable — not 'hard to guard', actually unguardable. 4 rings and the most dominant stretch of Finals basketball (2000-2002) you'll ever see."]),

    (r'\b(magic\s+johnson|earvin\s+johnson)\b',
     [r"\1 was 6'9\" and played point guard better than anyone who ever lived. In his rookie year he played all 5 positions in a single Finals game because Kareem was injured — and dropped 42 points, 15 rebounds and 7 assists. He was 20 years old. 5 championships, 3 MVPs, and he and Larry Bird basically saved the NBA from irrelevance in the 1980s.",
      r"If you want to understand what made \1 special, watch old Lakers tape and just track where his eyes go. He saw the whole floor like a chess player. 5 rings, a smile that could light up an arena, and a rivalry with Bird that turned the NBA into must-watch television."]),

    (r'\b(larry\s+bird|larry\s+legend)\b',
     [r"\1 was the kind of player who'd tell you exactly what he was about to do to you — and then do it anyway. 3 consecutive MVPs (1984-86), 3 championships with the Celtics, and a trash-talking game so elite it's still quoted today. Came from French Lick, Indiana and became one of the 5 best players to ever touch a basketball.",
      r"\1 was ice cold. 3 MVPs, 3 rings, and the kind of clutch gene that made coaches trust him with the ball when everything was on the line. His rivalry with Magic Johnson didn't just sell tickets — it rescued a league that was struggling for relevance."]),

    (r'\b(kareem\s+abdul-?jabbar|kareem)\b',
     [r"\1 held the NBA scoring record for 38 years — from 1984 until LeBron finally passed him in 2023. Let that sink in. 6 championships, 6 MVPs (both still the most in NBA history), and a skyhook shot so mechanically perfect that in 20 years of playing it, nobody ever figured out how to stop it. He's the quiet blueprint that every big man since has tried to copy.",
      r"People sleep on \1 because he wasn't flashy, but the numbers don't lie. All-time scoring leader for nearly four decades, 6 rings, 6 MVPs, and the most unstoppable shot in basketball history. The skyhook wasn't just a move — it was a career."]),

    (r'\b(giannis(\s+antetokounmpo)?|greek\s+freak)\b',
     [r"\1 came to the NBA from Greece as a teenager who could barely speak English, and turned himself into the most physically terrifying player in the league. 2021 championship, Finals MVP, and a 50-point performance in the clinching game that made everyone watching feel like they'd witnessed something they'd describe to their grandkids. 2 regular season MVPs, Defensive Player of the Year, and he's still not done.",
      r"The 'Greek Freak' nickname for \1 is almost an understatement. 6'11\" with the wingspan of a small aircraft, handles like a guard, and a motor that never stops. His 2021 Finals run was one of the most dominant postseason performances of the modern era."]),

    (r'\b(kevin\s+durant|kd)\b',
     [r"\1 is 6'10\" with guard skills, a 7'5\" wingspan, and the ability to score from literally anywhere on the floor. Defenders have described guarding him as a nightmare with no good options. 2 championships with Golden State, 2 Finals MVPs, and a scoring ability so pure that even his harshest critics have to nod in respect.",
      r"There's a reason coaches say \1 might be the hardest player in NBA history to gameplan against. Too tall for guards, too skilled for bigs, and too relentless for everyone else. 2 rings, 2 Finals MVPs, 2014 regular season MVP, and a scoring résumé that belongs in a museum."]),

    (r'\b(tim\s+duncan|big\s+fundamental)\b',
     [r"\1 is proof that 'boring' and 'brilliant' can be the same thing. No dunks for show, no flashy plays — just perfect basketball, every single night, for 19 years. 5 championships, 2 regular season MVPs, 3 Finals MVPs, and he anchored a Spurs dynasty that spanned three different eras of the NBA. The 'Big Fundamental' is not an insult — it's the highest compliment in the game.",
      r"\1 is the greatest power forward who ever lived and somehow the most underrated superstar in NBA history at the same time. 5 rings all with San Antonio, never needed to leave, never needed the spotlight. Just showed up and won. Every single year."]),

    (r'\b(wilt\s+chamberlain|wilt|the\s+stilt)\b',
     [r"\1 scored 100 points in a single game on March 2, 1962. One hundred. He also averaged 50.4 points per game for that entire season. Not a game — a season. These are numbers so absurd that statisticians have questioned whether modern players could even approach them with today's pace and rules. He was 7'1\" with the athleticism of a small forward. Simply from another planet.",
      r"Every time someone calls an NBA record 'unbreakable', historians point to \1 and say 'that's nothing'. 100-point game. 50.4 PPG for a season. 2,149 free throws attempted in one year. The man didn't play basketball so much as he performed feats that the rest of us just watched in disbelief."]),

    (r'\b(hakeem(\s+olajuwon)?|the\s+dream)\b',
     [r"\1 — 'The Dream' — might have the best footwork of any player in NBA history regardless of position. Back-to-back championships in 1994 and 1995, Finals MVP both times, and his 'Dream Shake' post move was so devastating that coaches have studied tape of it for 30 years trying to figure out how to defend it. Spoiler: they still haven't.",
      r"\1 was so good defensively that he won Defensive Player of the Year and the MVP in the same season (1994). He's the all-time leader in blocked shots and led Houston to 2 titles while Michael Jordan was briefly retired. That timing will never not be a talking point."]),

    (r'\b(russell\s+westbrook|westbrook)\b',
     [r"\1 plays basketball like he has a personal vendetta against the other team. Pure, unfiltered aggression every single possession. He holds the all-time career triple-double record (200+) and averaged a triple-double for an entire season in 2017 — winning MVP in the process. Love his style or hate it, you can't ignore it.",
      r"Watching \1 play is like watching someone try to break basketball with their bare hands. The athleticism is absurd, the stats are historic, and the competitive intensity is genuinely intimidating. All-time triple-double king, full stop."]),

    (r'\b(dirk\s+nowitzki|dirk)\b',
     [r"\1 is the greatest European player in NBA history and one of the most quietly devastating scorers the league has ever seen. He invented the one-legged step-back fadeaway jumper — a shot that should be physically impossible to defend, and somehow isn't because of how cleanly he rises into it. 2011 championship, Finals MVP, 2007 regular season MVP, 21 years all with Dallas. A career of pure loyalty and craft.",
      r"What makes \1 so remarkable is that he won a championship at 32 years old by absolutely dismantling Miami's Big Three — LeBron, Wade, and Bosh — in the Finals. He averaged 26 points, shot 46% from three, and won Finals MVP. The whole world counted him out and he just... didn't care."]),

    (r'\b(chris\s+paul|cp3|point\s+god)\b',
     [r"\1 is called 'The Point God' and the nickname is completely earned. He can control the pace of a game like a conductor running an orchestra — speed it up, slow it down, make the defense guess, and then knife through them for a layup or dish to the open man. All-time steals leader and one of the most complete point guards to ever run an offense. The championship just never came, which is the one asterisk on an otherwise flawless legacy.",
      r"If basketball IQ were a stat, \1 would lead it by 20 points. He reads defenses in real time, never makes the same mistake twice, and has been one of the best players in the league for nearly two decades. The ring just keeps slipping away — which is the cruel irony of an otherwise perfect career."]),

    (r'\b(james\s+harden|the\s+beard)\b',
     [r"\1 turned the step-back three-pointer into one of the most feared weapons in the NBA. 2018 MVP, 3 consecutive scoring titles, and a season in 2018-19 where he averaged 36.1 points per game — the third-highest single-season average in NBA history. Also the most elite free-throw drawer the league has ever seen, which either impresses you or drives you crazy depending on who you root for.",
      r"Say what you want about \1's style of play — and plenty of people do — but the man could flat-out score. 2018 MVP, perennial All-Star, and a scorer with so many tools in his arsenal that defending him was basically an unsolvable puzzle. The beard is legendary. The step-back is legendary. The career is legendary."]),

    # Teams
    (r'\b(la\s+lakers|los\s+angeles\s+lakers|lakers)\b',
     [r"The \1 are basically the New York Yankees of basketball — 17 championships, purple and gold everywhere, and a roster history that reads like an NBA Hall of Fame exhibit. Kareem, Magic, Shaq, Kobe, LeBron — name another franchise that has housed that many all-timers. You can't. The most glamorous team in the sport, and they've mostly backed it up.",
      r"17 championships and counting. The \1 have spent most of NBA history as either the best team in the league or the most talked-about team in the league — sometimes both at the same time. Whether you love them or hate them, they're always must-watch television."]),

    (r'\b(boston\s+celtics|celtics)\b',
     [r"The \1 have 18 championships — the most in NBA history — and they're not shy about reminding you. Bill Russell won 11 of those rings in 13 seasons, which is a dynasty so dominant it makes everything else look modest by comparison. The rivalry with the Lakers is the defining storyline of NBA history. Green runs deep in Boston.",
      r"The \1 built their identity on toughness, team basketball, and winning when it matters. 18 titles, the Bill Russell era, the Bird era, the KG/Pierce era, and now Jayson Tatum carrying the torch. The banner collection in TD Garden is genuinely intimidating to opposing teams."]),

    (r'\b(golden\s+state\s+warriors|warriors)\b',
     [r"The \1 didn't just win championships — they changed the sport. Their 2015-16 team went 73-9 and made shooting from 30 feet look routine. 4 championships in 8 years with Curry, Thompson, and Draymond Green — a core that worked so well together that the NBA had to adjust the rules to try to slow them down. They created an era.",
      r"7 championships, but the modern \1 dynasty is what people remember. Curry shooting from the logo, Klay Thompson's 37-point quarter, Draymond Green being a menace on defense — it was beautiful basketball played at a speed and with a precision that the league hadn't seen before."]),

    (r'\b(chicago\s+bulls|bulls)\b',
     [r"The 1990s \1 are the gold standard of NBA dynasties. Two three-peats (1991-93, 1996-98) with Michael Jordan, Scottie Pippen, and Phil Jackson — a collection of talent and coaching genius that produced the most dominant decade any team has had in the modern era. The 1995-96 squad went 72-10 and is still argued as the greatest team ever assembled.",
      r"The \1 dynasty was Jordan, yes — but it was also Scottie Pippen, one of the most criminally underrated players in NBA history, and Phil Jackson's triangle offense executed to near perfection. 6 rings in 8 years with no losses in the Finals. That's not a dynasty, that's a stranglehold."]),

    (r'\b(miami\s+heat|heat)\b',
     [r"The \1 have 3 championships but more than that they have a culture — 'Heat Culture' is a genuine thing that scouts and executives around the league respect. They develop overlooked players, demand toughness, and compete every single night. Dwyane Wade in 2006, the Big Three in 2012-13, and Jimmy Butler turning the 2020 bubble into a personal showcase. They always find a way.",
      r"3 rings for the \1 but the 2006 title might be the most dramatic — Dwyane Wade carrying that team on his back, averaging 35 points in the last three games of the Finals to beat Dallas. Then the LeBron/Wade/Bosh era brought two more. South Beach knows how to win."]),

    (r'\b(san\s+antonio\s+spurs|spurs)\b',
     [r"The \1 are what every front office in basketball wants to be when it grows up. 5 championships between 1999 and 2014, all with Tim Duncan and Gregg Popovich — a coach-player pairing so effective that the 'Spurs Way' became a philosophy taught in coaching clinics worldwide. They drafted foreign players before it was cool, developed role players into stars, and just quietly won. It's almost unfair how good they were at it.",
      r"No team in NBA history has been as consistently excellent for as long as the \1 under Popovich. 5 rings, zero drama, maximum results. They never had the flashiest roster or the biggest market but they had the best system — and the best system almost always wins."]),

    (r'\b(milwaukee\s+bucks|bucks)\b',
     [r"The \1 have 2 championships but their 2021 run deserves to be talked about more than it is. Giannis was written off after losing to Miami in the bubble and came back and won it all — then in the clinching Game 6 dropped 50 points, 14 rebounds, and 5 blocks. On the road. In the Finals. The 'Greek Freak' silenced every single critic in one night.",
      r"The \1 won their first title in 1971 with a 24-year-old Kareem Abdul-Jabbar who was so unstoppable that the league actually banned the dunk temporarily to slow him down. Then 50 years later Giannis won them another one. Milwaukee is a basketball city and always has been."]),

    (r'\b(dallas\s+mavericks|mavericks|mavs)\b',
     [r"The \1 2011 championship is one of the best underdog stories in NBA history. Dirk Nowitzki — then 32 and supposedly past his prime — dismantled LeBron, Wade, and Bosh's Miami superteam in 6 games, personally averaging 26 points and shooting 46% from three in the series. The whole basketball world had counted Dallas out. Dirk didn't get the memo.",
      r"The \1 have Dirk's ring in the trophy case and now they're building around Luka Dončić, who at 25 is already one of the most statistically dominant players in NBA history. Different eras, same city, same fearless style. Dallas basketball has an identity."]),

    (r'\b(denver\s+nuggets|nuggets)\b',
     [r"The \1 waited a long time for their first championship and when it finally came in 2023 it was delivered by Nikola Jokić — a 3-time MVP center who was drafted in the second round of the 2014 draft after reports surfaced that he was eating too many Snickers bars. From that moment to 3 MVPs and a Finals MVP might be the best glow-up in sports history.",
      r"Nikola Jokić and the \1 winning it all in 2023 was deeply satisfying for basketball purists. No superteam, no drama, no demanding trades — just a genius basketball player being a genius and a team that played together beautifully. Old-school excellence."]),

    (r'\b(toronto\s+raptors|raptors)\b',
     [r"The \1 are the NBA's only Canadian team and they made their one championship count. In 2019 Kawhi Leonard — a man whose facial expression has never changed in recorded history — went completely berserk in the playoffs, including THE shot against Philadelphia that bounced on the rim four times before going in. Toronto lost their minds. The whole country of Canada lost their minds. Worth it.",
      r"The \1 2019 championship run is one of the great 'right place, right time' stories in NBA history. They got Kawhi Leonard in a trade, he had one healthy season, led them to the title, then left for LA in free agency. One glorious year, one banner, and a moment every Canadian basketball fan will never forget."]),

    # Rules
    (r'\bhow\s+many\s+(quarters|periods)\b|\b(quarters)\s+in\s+(?:a\s+|an\s+)?(?:basketball|nba)\b',
     [r"An NBA game has 4 quarters of 12 minutes each — so 48 minutes of regulation basketball. College uses two 20-minute halves because apparently 4 quarters was too straightforward. If it's tied at the end, you play 5-minute overtime periods until someone wins. There are no ties in basketball.",
      r"4 quarters, 12 minutes each. If you end regulation tied, you keep playing 5-minute overtimes until someone pulls ahead — and if you've ever watched a 3OT playoff game at midnight on a Tuesday, you know it's both exhausting and incredible."]),

    (r'\bhow\s+many\s+players\s+(?:on|per|in)\s+(?:a\s+|the\s+)?(?:team|court|floor)\b',
     [r"5 players per side on the court at all times. NBA rosters hold 15 players total, 13 active on game night. The 5 positions are point guard, shooting guard, small forward, power forward, and center — though modern basketball has mostly dissolved those labels into just 'can you guard multiple positions and shoot threes?'",
      r"5 on 5 — that's the game. 15-man rosters with 13 active per game. The classic positions are PG, SG, SF, PF, and C but in the modern NBA 'positionless basketball' means everybody is expected to do a bit of everything."]),

    (r'\b(three.?point|3.?point)\s+(?:line|shot|arc|rule)\b',
     [r"The NBA three-point line sits 23 feet 9 inches from the basket at the top of the arc, 22 feet in the corners. Make a shot from beyond it and it's worth 3 points instead of 2 — a rule introduced in 1979-80 that the rest of the world thought was a gimmick. Then Steph Curry happened and now teams shoot 35 threes a game and the league looks completely different.",
      r"The \1 line changed basketball more than any other rule in the sport's history. Introduced in 1979, mostly ignored for two decades, then fully weaponized by players like Steph Curry and Ray Allen until every team in the league built their entire offense around it. 23'9\" from the basket — a line that rewrote the game."]),

    (r'\bhow\s+does\s+scoring\s+work\b|\bpoint\s+values\b|\bscoring\s+rules\b',
     [r"Inside the three-point arc = 2 points, beyond the arc = 3 points, free throw = 1 point. Simple in theory, endlessly complex in practice. The team with the most points at the final buzzer wins. A shot counts if the ball leaves your hand before time expires — which is why you see players launching prayers at the horn.",
      r"2 for a field goal inside the arc, 3 from beyond it, 1 per free throw. The buzzer just has to catch the ball leaving your hand, not in the air — which is why buzzer-beaters are so dramatic. Most points wins. It's simple, beautiful, and brutal."]),

    (r'\bwhat\s+is\s+(?:a\s+)?(?:personal\s+)?(foul)\b|\bhow\s+do\s+(foul)s?\s+work\b',
     [r"A personal \1 is illegal physical contact — holding, pushing, hitting, blocking illegally. In the NBA you're allowed 6 before you're disqualified, which is called 'fouling out'. Get fouled while shooting and you get free throws: 2 for a regular shot, 3 if it was a three-point attempt. Teams also enter the 'bonus' after 5 team fouls per quarter, meaning any foul sends the opponent to the line.",
      r"Foul someone while they're shooting and they get free throws. Commit 6 personal fouls in a game and you're done — ejected. NBA refs have gotten more foul-happy over the years, which is either 'protecting players' or 'ruining the flow of the game' depending on who you ask."]),

    (r'\b(shot\s+clock)\b',
     [r"The NBA \1 is 24 seconds. You get the ball, you have 24 seconds to attempt a shot that hits the rim or the basket — otherwise it's a violation and the other team gets possession. It resets to 14 seconds after certain offensive rebounds. The \1 was introduced in 1954 because before it existed teams would just... hold the ball and not shoot. Imagine watching that.",
      r"24 seconds on the \1 — use them or lose possession. It was invented in 1954 by Danny Biasone who literally calculated the ideal pace of play by dividing seconds in a game by average shots taken. Without it, basketball would be an entirely different sport. Thank Danny."]),

    (r'\b(traveling|travel\s+violation)\b',
     [r"\1 is taking too many steps without dribbling. You get 2 steps after gathering the ball to shoot or pass — a rule that sounds simple until you watch slow-motion replays and realize the NBA's definition of 'gathering' is extremely generous. The Euro step (one direction, then the other) is a perfectly legal 2-step move that looks like traveling and technically isn't.",
      r"The \1 violation is one of the most debated calls in basketball because the rules around the 'gather step' are genuinely complicated. Short version: 2 steps after you pick up your dribble, otherwise it's a violation. The longer version involves the exact moment the ball 'rests' in your hand, which refs interpret with a lot of... flexibility."]),

    (r'\b(goaltending)\b',
     [r"\1 is when a defender touches a shot that's on its downward arc toward the basket, or touches the ball while it's sitting on or above the rim. The offense gets the points automatically, as if it went in. It's a brutal call to have made against you because there's no discretion — if the ref sees it, the points go up, no questions asked.",
      r"\1 is one of the few absolute calls in basketball — if a defender touches a shot on the way down or above the cylinder, the basket counts, period. No appeal, no discussion. It punishes shot-blockers who time their jumps slightly wrong and rewards shooters who can arc the ball high enough to trigger it."]),

    (r'\b(technical\s+foul|tech\s+foul)\b',
     [r"A \1 is called for unsportsmanlike conduct that doesn't involve physical contact — arguing with referees, taunting opponents, throwing your mouthpiece, general theatrics. The other team gets 1 free throw and possession. Get 2 in a game and you're automatically ejected. Some players collect technicals like trading cards. Draymond Green is essentially their mascot.",
      r"A \1 is the referee's way of saying 'calm down or leave'. 1 free throw for the other team, and a second tech means you're ejected. The NBA fines players per technical after a certain threshold — meaning some guys are paying thousands of dollars per argument. Remarkably, some of them keep arguing anyway."]),

    (r'\b(flagrant\s+foul)\b',
     [r"A \1 is unnecessary or excessive contact — the kind that goes beyond trying to stop a play and starts looking like you just don't like the other person. Flagrant 1 is hard but not intentional: 2 free throws plus possession. Flagrant 2 is deemed reckless or intentional: automatic ejection plus potential suspension. It's the NBA's way of saying 'we saw what you did there'.",
      r"\1 fouls are the ones that make everyone in the arena go quiet for a second. Flagrant 1 means it was nasty but not necessarily dirty — 2 free throws and possession. Flagrant 2 means the refs decided it crossed a line — you're gone, and the league will probably have some words for you by Monday."]),

    (r'\b(backcourt\s+violation|over.and.back)\b',
     [r"A \1 is when your team brings the ball across half-court into the frontcourt and then sends it back to the backcourt — whether by pass, dribble, or deflection. Once you cross that line going forward, you're committed. Cross it back and the other team gets the ball. It's the basketball equivalent of no take-backs.",
      r"Once you cross half-court, that's your side now. A \1 is called when the offense retreats into the backcourt after establishing the frontcourt — turnover, other team's ball. It forces teams to push forward and is one of the reasons full-court traps can be so effective in the final minutes."]),

    # History & Structure
    (r'\bwho\s+invented\s+(basketball)\b|\bhistory\s+of\s+(basketball)\b|\bwhen\s+was\s+(basketball)\s+invented\b',
     [r"\1 was invented by Dr. James Naismith in December 1891 in Springfield, Massachusetts. He was a PE teacher who needed an indoor winter activity, nailed two peach baskets to a balcony, wrote 13 rules in an afternoon, and accidentally created one of the most popular sports on the planet. The first game had 9 players per side and the baskets didn't even have holes — someone had to climb up and retrieve the ball every time someone scored.",
      r"Dr. James Naismith invented \1 in 1891 in a Massachusetts gym with a soccer ball and two peach baskets. He was trying to keep students active indoors during winter. 130 years later it's a global sport generating billions of dollars and has produced some of the most famous athletes in human history. Not bad for an afternoon's worth of rule-writing."]),

    (r'\bwhen\s+was\s+(?:the\s+)?(nba)\s+founded\b|\b(nba)\s+(?:history|founded|founding)\b',
     [r"The \1 was founded on June 6, 1946 — originally called the Basketball Association of America (BAA) — before merging with the rival National Basketball League (NBL) in 1949 to become the NBA. It started with 11 teams and now has 30 spanning the US and Canada. For context, in its early years games were sometimes played in front of a few hundred people. Now the Finals draws 15 million viewers.",
      r"The \1 started in 1946 as the BAA and became the NBA in 1949 after merging with the NBL. The league spent its early decades struggling for relevance — baseball and boxing were bigger deals in America. Then Magic vs Bird in the '80s and Jordan in the '90s turned it into a global phenomenon. Now it's the third-highest revenue sports league on Earth."]),

    (r'\bhow\s+many\s+teams\s+(?:in|does)\s+(?:the\s+)?(nba)\b',
     [r"The \1 has 30 teams split into two conferences of 15 — Eastern and Western. Each conference has three divisions of 5 teams. The only non-American franchise is the Toronto Raptors, who represent all of Canada and won the championship in 2019, which caused the kind of national celebration Canada usually reserves for hockey.",
      r"30 teams, 15 per conference. East and West each have three divisions. Toronto is the only Canadian franchise — they're also the only team to have won a championship while all the other contenders lost a player to a potentially season-ending injury in the process. 2019 was wild."]),

    (r'\b(nba\s+playoffs|playoffs|postseason)\b|\bhow\s+do\s+the\s+(playoffs)\s+work\b',
     [r"The \1 take the top 8 teams from each conference — though now there's a play-in tournament for seeds 7 through 10, which either adds drama or ruins the regular season depending on your philosophy. Then it's four rounds of best-of-7 series: First Round, Conference Semifinals, Conference Finals, NBA Finals. You need 16 wins to hoist the trophy. It's a grind.",
      r"16 teams make the \1 — 8 from each conference via the regular season standings plus a play-in tournament for the bubble teams. Then best-of-7 all the way through: First Round, Semis, Conference Finals, Finals. Win 16 games to be champion. The two-month gauntlet separates the good teams from the great ones."]),

    (r'\b(nba\s+draft)\b|\bhow\s+does\s+the\s+(draft)\s+work\b',
     [r"The \1 is held every June — 2 rounds, 30 picks each, 60 players total selected from college, international leagues, and high school (rare). Teams with worse records get better odds in the draft lottery for top picks — theoretically incentivizing losing, which the NBA has tried to fix with the lottery system several times. Recent top picks: Victor Wembanyama went #1 in 2023 after being called the most unique prospect in NBA history.",
      r"The \1 is two rounds of 30 picks each. Worse records in the regular season mean better lottery odds for high picks — the idea being that bad teams get help to get better. It doesn't always work that way, but it's the theory. Getting the #1 pick can genuinely change a franchise, as any San Antonio fan watching Victor Wembanyama will tell you."]),

    # Stats & Awards
    (r'\b(mvp|most\s+valuable\s+player)\b',
     [r"The NBA \1 award is voted on by sportswriters and broadcasters — which means it's occasionally controversial, almost always argued about, and endlessly fun to debate. Kareem holds the record with 6. Jordan, LeBron, and Moses Malone have 4 each. Nikola Jokić has won 3 in a 4-year span, which at this point seems like it might just be his award to lose.",
      r"6 MVPs for Kareem — the record. 4 each for Jordan, LeBron, and Moses Malone. Then there's Nikola Jokić with 3 in recent years, Russell Westbrook with 1 that people still debate, and Steph Curry with 2 including the only unanimous vote in league history. The \1 race is the NBA's best annual argument."]),

    (r'\b(triple.?double)\b|\bwhat\s+is\s+a\s+(triple.?double)\b',
     [r"A \1 means hitting double digits in three statistical categories in one game — usually points, rebounds, and assists. It's relatively rare because it requires being good at multiple things at once, which is harder than it sounds. Russell Westbrook holds the all-time career record (200+) and averaged one for an entire season in 2017, winning MVP. Oscar Robertson did it first, for a full season, in 1961-62, and nobody believed it until they checked the stats.",
      r"A \1 is 10+ points, 10+ rebounds, and 10+ assists in a single game — the basketball Swiss Army knife stat. Russ Westbrook has the career record and made it look almost routine for a stretch. The rarest version is points/steals/blocks, which happens maybe once every few years and breaks the internet when it does."]),

    (r'\bwhat\s+is\s+an?\s+(assist)\b|\b(assist)s?\s+in\s+basketball\b',
     [r"An \1 is a pass that directly leads to a made basket — your read, their bucket, shared credit. John Stockton holds the all-time record with 15,806 career \1s, which is so far ahead of second place that it's almost its own category. Magic Johnson turned the \1 into an art form. Chris Paul turned it into a science.",
      r"The \1 is basketball's most collaborative stat — you get credit for making the pass that set up the score. John Stockton's 15,806 career \1s is one of those records that seems completely unreachable. For context, second place on the all-time list is 4,000 behind him."]),

    (r'\bwhat\s+is\s+an?\s+(rebound)\b|\b(rebound)s?\s+in\s+basketball\b',
     [r"A \1 is grabbing the ball after a missed shot — offensive if it was your team's miss, defensive if it was the other team's. Offensive \1s are gold because they give you another possession; defensive \1s just end the opponent's. Wilt Chamberlain holds the career record with 23,924, which is another one of those numbers that makes you feel like he was just operating on a different plane of existence.",
      r"Grab the ball after a missed shot and that's a \1. Sound simple? It isn't — it requires positioning, timing, physicality, and basketball IQ. Dennis Rodman won 7 consecutive rebounding titles despite being 6'7\" because he studied shooters' misses so carefully he knew where the ball was going before it left their hands."]),

    (r'\bwhat\s+is\s+an?\s+(block|blocked\s+shot)\b|\b(block)s?\s+in\s+basketball\b',
     [r"A \1 is legally deflecting a field goal attempt — you have to be clean about it, no hitting the arm, no touching the ball on its way down. Hakeem Olajuwon holds the all-time record and is widely considered the best shot-blocker in history because he didn't just knock the ball out of bounds — he directed his \1s to teammates to start fast breaks. Dikembe Mutombo made the finger wag after every \1 and it became one of the most iconic celebrations in sports.",
      r"A \1 is when you legally deflect someone's shot attempt and it's one of the most electric plays in basketball. Hakeem holds the record. Dikembe Mutombo made the finger wag famous. And there are few sounds in sports more satisfying than a clean \1 at the rim."]),

    (r'\bwhat\s+is\s+an?\s+(steal)\b|\b(steal)s?\s+in\s+basketball\b',
     [r"A \1 is legally taking the ball from the ball-handler — picking a pocket, deflecting a pass, or reading a play before it happens. John Stockton holds the all-time record with 3,265 career \1s, which tracks because Stockton was basically a defensive menace disguised as a point guard. Chris Paul is the active king and Gary Payton 'The Glove' made it a calling card.",
      r"The \1 is the most disrespectful defensive play in basketball — you saw it coming, they didn't, and now it's your ball. Stockton holds the record. Gary Payton was nicknamed 'The Glove' because the ball just couldn't get past him. A well-timed \1 can swing the entire momentum of a game."]),

    (r'\b(all.?star)\s*(?:game|weekend|break)?\b|\bnba\s+(all.?star)\b',
     [r"The NBA \1 Game is in February — East vs West, voted in by fans, players, and media. The game itself is notoriously low-effort defense and extremely high-effort dunking, which is honestly fine because it's an exhibition and nobody signed up for real basketball. \1 Weekend is the real event: Slam Dunk Contest, Three-Point Contest, Skills Challenge, and enough celebrity sightings to fill a tabloid for a month.",
      r"\1 Weekend is the NBA's annual party — the game is mostly an excuse for highlights, but the Dunk Contest, Three-Point Contest, and Rising Stars Game are legitimately exciting. Michael Jordan's dunk from the free-throw line in 1988 and Vince Carter's 2000 performance are the two greatest Dunk Contest moments and people still argue about which was better."]),

    # Records
    (r'\b(scoring\s+record|all.?time\s+scoring)\b|\bmost\s+points\s+(?:ever|career)\b',
     [r"LeBron James holds the NBA career \1 with 40,000+ points, passing Kareem Abdul-Jabbar's 38,387 in February 2023 — a record Kareem had held for 38 years. LeBron did it at 38 years old, which says everything about his longevity. For single-game records though, Wilt Chamberlain's 100-point game in 1962 sits completely alone and will probably stay there.",
      r"The all-time career scoring record belongs to LeBron James (40,000+ points) after he passed Kareem in 2023. The single-game record belongs to Wilt Chamberlain (100 points in 1962) and will almost certainly never be broken because nothing about that game made any logical sense."]),

    (r'\b100.?point\s+game\b|\bwilt.*?100\b',
     [r"March 2, 1962. Hershey, Pennsylvania. Wilt Chamberlain scored 100 points for the Philadelphia Warriors against the New York Knicks. There's no official game footage — just a box score, a single blurry photo of Wilt holding a paper with '100' written on it, and decades of disbelief. He made 36 of 63 field goals and 28 of 32 free throws. The Knicks tried intentionally fouling other Warriors players to stop him from shooting. It didn't work.",
      r"100 points. One game. Wilt Chamberlain. March 2, 1962. He also averaged 50.4 points per game for that entire season. These are numbers so removed from reality that they still generate arguments 60 years later. No one has come within 30 points of the single-game record since. It might genuinely be the most unbreakable record in all of sports."]),

    (r'\bmost\s+(championships|rings|titles)\b|\bwho\s+has\s+the\s+most\s+(rings|titles)\b',
     [r"Bill Russell has the most individual \1 with 11 in 13 seasons with the Celtics between 1957 and 1969. Eleven. In thirteen years. He's also the reason the Celtics have the most franchise \1 at 18 — though the Lakers are close behind with 17. Russell's \1 total is another one of those records that seems designed to be permanent.",
      r"Bill Russell: 11 \1. In 13 seasons. With the Celtics. As a franchise the Celtics lead with 18 total, the Lakers have 17. As an individual, nobody is touching Russell's 11 — Jordan's 6 looks modest by comparison, which tells you everything about how dominant those Celtics teams were."]),

    (r'\bbest\s+(?:season\s+)?record\s+(?:ever|in\s+nba)\b|\b73.?9\b|\b72.?10\b',
     [r"Golden State went 73-9 in 2015-16, breaking the Chicago Bulls' 72-10 record from 1995-96. They celebrated that accomplishment and then promptly blew a 3-1 lead in the Finals against LeBron's Cavaliers — one of the great collapses in sports history. They have 4 championships. They will never fully live down not winning that year.",
      r"73-9 for Golden State in 2015-16 — the best regular season record in NBA history. The Bulls went 72-10 in 1995-96 and won the championship. The Warriors went one better and lost the Finals. The universe has a sense of humor."]),

    # General
    (r'\bwho\s+is\s+the\s+(?:best|greatest|goat)\b|\b(goat)\s+debate\b|\bjordan\s+vs\s+lebron\b|\blebron\s+vs\s+jordan\b',
     [r"The Jordan vs LeBron GOAT debate is the gift that keeps giving — both sides are right and both sides are wrong and it will never be resolved. Jordan: 6 rings, 6-0 in the Finals, never lost a championship series, 30.1 career PPG. LeBron: 4 rings with 3 different teams, all-time scoring record, still playing at 40. Jordan fans say perfection matters. LeBron fans say longevity and versatility matter more. Both arguments are airtight. Pick your poison.",
      r"Ask 10 NBA experts who the GOAT is and 5 say Jordan, 4 say LeBron, and 1 says something interesting. Jordan's case: 6-0 in the Finals, 6 Finals MVPs, never needed a Game 7. LeBron's case: 4 rings across 3 teams spanning 20 years, all-time scoring record, arguably more complete player. The debate is eternal and honestly that's part of what makes the NBA great."]),

    (r'\b(position)s?\s+in\s+basketball\b|\bbasketball\s+(position)s?\b|\bwhat\s+are\s+the\s+(position)s\b',
     [r"Traditionally 5 \1s: Point Guard (runs the offense, usually the smartest player on the floor), Shooting Guard (scoring, perimeter shooting), Small Forward (versatile, does a bit of everything), Power Forward (physical, interior presence), Center (tallest, protects the rim, anchors the paint). In modern basketball the lines have blurred almost completely — now the question is just 'can you do multiple things?'",
      r"The 5 classic \1s: PG (floor general), SG (scorer), SF (versatile wing), PF (power inside), C (rules the paint). Modern NBA has basically dissolved these into 'wings' and 'bigs' because positionless basketball means a 6'8\" player might be running the offense while a guard guards the center. Positions are more of a suggestion now."]),

    (r'\bwhat\s+is\s+(basketball)\b|\bhow\s+(?:do\s+you\s+)?play\s+(basketball)\b',
     [r"\1 is 5 vs 5, shoot the ball through a 10-foot hoop to score points. Most points after 4 quarters wins. Simple enough that Dr. Naismith wrote the rules in an afternoon in 1891, complex enough that coaches still argue about offensive schemes at 2am. The NBA is the world's top professional \1 league — 30 teams, 82-game regular season, and a playoffs system that somehow produces drama every single year.",
      r"Two teams of 5, one ball, two hoops at opposite ends of the court. Score more points than the other team in 48 minutes and you win. \1 looks simple from the outside and reveals infinite complexity the deeper you go into it — which is why people have been obsessed with it for over 130 years."]),

    # Meta
    (r'\bwhat\s+can\s+you\s+(?:do|help|tell)\b|\bhelp\b',
     [r"I'm your personal NBA encyclopedia — rule-based, regex-powered, and basketball-obsessed. Ask me about: 🏀 Players (LeBron, Jordan, Kobe, Curry, Shaq, Giannis, Wilt, anyone) | 🏆 Teams (Lakers, Celtics, Warriors, Bulls, Spurs, and more) | 📋 Rules (fouls, shot clock, traveling, goaltending...) | 📜 History & Records | 🎯 Stats & Awards. Go ahead — stump me.",
      r"Glad you asked! I know about NBA players, teams, rules, history, records, and stats. Try asking: 'Who is the GOAT?', 'Tell me about the Spurs dynasty', 'What is goaltending?', or 'How many teams are in the NBA?' — I've got 56+ rules and a deep love of basketball."]),

    (r'\b(thanks?|thank\s+you|thx|ty)\b',
     [r"Nothing but net! 🏀 Ask me anything else — I'm here all season.",
      r"Anytime. That's what I'm here for. More basketball questions?",
      r"Easy bucket. What else do you want to know?"]),

    (r'\b(bye|goodbye|see\s+ya|later|peace|farewell)\b',
     [r"See you later! Come back when you want more hoops knowledge — the doors are always open 🏀",
      r"Goodbye! Go watch some basketball. You won't regret it. 🏆",
      r"Later! And remember — ball is life 🏀"]),
]


def normalize(text):
    text = re.sub(r"\bwho\'?s\b",   "who is",   text, flags=re.IGNORECASE)
    text = re.sub(r"\bwhat\'?s\b",  "what is",  text, flags=re.IGNORECASE)
    text = re.sub(r"\bhow\'?s\b",   "how is",   text, flags=re.IGNORECASE)
    text = re.sub(r"[^\w\s']",      " ",         text)
    text = re.sub(r"\s+",           " ",         text).strip()
    return text


def get_response(user_input):
    text = normalize(user_input)
    for pattern, templates in RULES:
        if re.search(pattern, text, re.IGNORECASE):
            template = random.choice(templates)
            result = re.sub(pattern, template, text, count=1, flags=re.IGNORECASE)
            return result[0].upper() + result[1:] if result else result
    return (
        "Hmm, didn't catch that one! I know about NBA players, teams, rules, history, and records. "
        "Try something like 'Who is Kobe Bryant?' or 'How does the shot clock work?' — I've got answers."
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok", "rules": len(RULES)})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or not data.get("message", "").strip():
        return jsonify({"error": "No message provided"}), 400
    return jsonify({"response": get_response(data["message"])})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
