import init_django_orm  # noqa: F401
import json

from db.models import Race, Skill, Player, Guild


def create_or_update_race(race_data: dict) -> Race:
    race_description = race_data.get("description")
    if race_description is None:
        return (Race.objects.get_or_create(name=race_data["name"]))[0]
    return (Race.objects.get_or_create(
        name=race_data["name"],
        description=race_description)
    )[0]


def create_or_update_guild(guild_data: dict) -> Guild | None:
    if not guild_data:
        return None
    guild_description = guild_data.get("description")
    return Guild.objects.get_or_create(
        name=guild_data["name"],
        description=guild_description
    )[0]


def create_or_update_skill(skill_data: dict, race: Race) -> None:
    Skill.objects.get_or_create(
        name=skill_data["name"],
        bonus=skill_data["bonus"],
        race=race)


def create_player(
        nickname: str,
        email: str,
        bio: str,
        race: Race,
        guild: Guild
) -> None:
    Player.objects.create(
        nickname=nickname,
        email=email,
        bio=bio,
        race=race,
        guild=guild
    )


def main() -> None:
    with open("players.json", "r") as file:
        players = json.load(file)

    for player_name, player_data in players.items():
        print(player_data["race"]["skills"])

        race = create_or_update_race(player_data["race"])
        guild = create_or_update_guild(player_data.get("guild"))

        for skill_data in player_data["race"]["skills"]:
            create_or_update_skill(skill_data, race)

        create_player(
            nickname=player_name,
            email=player_data["email"],
            bio=player_data["bio"],
            race=race,
            guild=guild
        )


if __name__ == "__main__":
    main()
