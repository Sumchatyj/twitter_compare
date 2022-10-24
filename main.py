import requests
import csv


HEADERS = {
    "User-Agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 "
                  f"Safari/537.36",
    "authorization" : f"Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E"
                      f"6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33"
                      f"AGWWjCpTnA",
}

GUEST_TOKEN_URL = "https://api.twitter.com/1.1/guest/activate.json"

def generate_user_url(username: str):
    return (
        f"https://twitter.com/i/api/graphql/HThKoC4xtXHcuMIok4O0HA/"
        f"UserByScreenName?variables=%7B%22screen_name%22%3A%22"
        f"{username}%22%2C%22withSafetyModeUserFields%22%3Atrue"
        f"%2C%22withSuperFollowsUserFields%22%3Atrue%7D&features=%7B%22"
        f"verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_"
        f"graphql_timeline_navigation_enabled%22%3Atrue%7D"
    )


def main():
    guest_token_response = requests.post(GUEST_TOKEN_URL, headers=HEADERS)
    token = guest_token_response.json().get('guest_token')
    users = []
    users.append(str(input("enter first twitter username: ")))
    users.append(str(input("enter second twitter username: ")))
    result = []
    for user in users:
        HEADERS["x-guest-token"] = token
        response = requests.get(
            generate_user_url(user),
            headers=HEADERS
        )
        user_list = [user, ]
        created_at = response.json().get('data').get('user').get('result').get('legacy').get('created_at')
        created_at_list = created_at.split()
        created_at_list.pop(4)
        created_at_list.pop(3)
        created_at_list.pop(0)
        created_at_str = ' '.join(created_at_list)
        user_list.append(created_at_str)
        user_list.append(response.json().get('data').get('user').get('result').get('legacy').get('followers_count'))
        result.append(user_list)
    header = ('username', 'created_at', 'followers_count')
    with open(f'{users[0]}_vs_{users[1]}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for user in result:
            writer.writerow(user)


if __name__ == "__main__":
    main()