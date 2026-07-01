from django.core.management.base import BaseCommand
from django.utils.text import slugify

from posts.models import Post

NEWS = [
    {
        "title": "Flexi Foods yafunguliwa rasmi Kimara",
        "body": "Kampuni ya Flexi Foods imefungua tawi jipya Kimara, ikiwaletea "
                "wakazi huduma ya kupanga milo kwa wagonjwa wa kisukari. Mfumo "
                "huo ulitengenezwa na kijana wa Kitanzania na tayari unatumika "
                "katika hospitali kadhaa jijini.",
    },
    {
        "title": "Daraja jipya la Kigamboni laongeza kasi ya usafiri",
        "body": "Wasafiri kati ya Kigamboni na katikati ya jiji sasa wanatumia "
                "muda mfupi baada ya kufunguliwa kwa njia mpya. Mamlaka "
                "inasema msongamano umepungua kwa zaidi ya nusu wakati wa asubuhi.",
    },
    {
        "title": "Wakulima wa Morogoro wapata soko la uhakika la mpunga",
        "body": "Kupitia ushirika mpya, wakulima wa mpunga wilayani Morogoro "
                "wameingia mkataba wa kuuza mazao yao moja kwa moja kwa "
                "wanunuzi wakubwa, jambo linaloahidi bei bora msimu huu.",
    },
    {
        "title": "Timu ya taifa yajiandaa kwa mashindano ya ukanda",
        "body": "Kikosi cha taifa kimeanza kambi ya mafunzo jijini Dar es Salaam "
                "kikijiandaa na mashindano ya ukanda yanayotarajiwa kuanza "
                "mwezi ujao. Kocha amesema ana matumaini makubwa na vijana wapya.",
    },
    {
        "title": "Huduma za afya za mtandaoni zaanza mikoani",
        "body": "Wizara ya afya imezindua mfumo unaowawezesha wananchi kupata "
                "ushauri wa daktari kwa njia ya simu. Huduma hiyo inaanza katika "
                "mikoa mitano kabla ya kusambazwa nchi nzima.",
    },
    {
        "title": "Wanafunzi wabuni programu ya kutabiri mvua",
        "body": "Kikundi cha wanafunzi wa chuo kikuu kimebuni programu inayotumia "
                "takwimu za hali ya hewa kutabiri mvua kwa usahihi wa hadi siku "
                "saba. Wanatarajia kuwasaidia wakulima kupanga kilimo chao.",
    },
    {
        "title": "Soko jipya la kisasa lafunguliwa Mbeya",
        "body": "Wafanyabiashara wa Mbeya wamepata soko jipya la kisasa lenye "
                "maghala, majokofu na eneo la maegesho. Halmashauri inasema "
                "litarahisisha biashara na kupunguza upotevu wa mazao.",
    },
    {
        "title": "Mtandao wa maji safi wafika vijiji vya Dodoma",
        "body": "Mradi wa maji umefanikiwa kufikisha maji safi na salama katika "
                "vijiji kumi mkoani Dodoma. Wakazi sasa hawatembei umbali mrefu "
                "kutafuta maji, jambo linalowapa muda wa shughuli nyingine.",
    },
    {
        "title": "Klabu za mpira zaanza msimu mpya wiki ijayo",
        "body": "Ligi kuu itaanza rasmi wiki ijayo huku timu zikimalizia "
                "maandalizi. Mashabiki wanatarajia msimu wa ushindani mkali "
                "baada ya klabu kadhaa kusajili wachezaji wapya.",
    },
    {
        "title": "Wajasiriamali vijana wapata mafunzo ya teknolojia",
        "body": "Zaidi ya wajasiriamali mia mbili wamehitimu mafunzo ya "
                "teknolojia na biashara mtandaoni jijini Arusha. Waandaaji "
                "wanasema lengo ni kukuza ajira kwa vijana.",
    },
    {
        "title": "Barabara ya mzunguko yapunguza foleni Mwanza",
        "body": "Ufunguzi wa barabara mpya ya mzunguko umepunguza kwa kiasi "
                "kikubwa msongamano wa magari katikati ya jiji la Mwanza "
                "hasa nyakati za asubuhi na jioni.",
    },
    {
        "title": "Kituo kipya cha afya chazinduliwa Tanga",
        "body": "Wakazi wa Tanga wamepata kituo kipya cha afya chenye vifaa "
                "vya kisasa. Huduma zitajumuisha uchunguzi wa magonjwa, "
                "chanjo na huduma ya mama na mtoto.",
    },
    {
        "title": "Maonyesho ya kilimo yavutia wakulima elfu kadhaa",
        "body": "Maonyesho ya kilimo yameanza rasmi yakiwakutanisha wakulima, "
                "watafiti na wafanyabiashara wa pembejeo. Wakulima wanapata "
                "fursa ya kujifunza mbinu mpya za kuongeza mavuno.",
    },
    {
        "title": "Mradi wa umeme jua waangazia shule za vijijini",
        "body": "Shule zaidi ya thelathini vijijini zimeunganishwa na umeme wa "
                "jua, jambo linalowawezesha wanafunzi kusoma hata usiku na "
                "kutumia vifaa vya kidijitali darasani.",
    },
    {
        "title": "Wavuvi wa Ziwa Victoria wapata boti za kisasa",
        "body": "Kikundi cha wavuvi kimekabidhiwa boti za kisasa zenye usalama "
                "zaidi. Mradi huu unatarajiwa kuongeza uvuvi salama na kipato "
                "cha wavuvi katika ukanda wa ziwa.",
    },
]


class Command(BaseCommand):
    help = "Seed the database with sample news posts."

    def handle(self, *args, **options):
        created = 0
        for item in NEWS:
            slug = slugify(item["title"])[:50].rstrip("-")
            _, was_created = Post.objects.get_or_create(
                slug=slug,
                defaults={"title": item["title"], "body": item["body"]},
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {created} new post(s). Total posts: {Post.objects.count()}."
        ))
