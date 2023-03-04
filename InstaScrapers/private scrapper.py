import instaloader
import json
import csv

# Create an instance of Instaloader class
L = instaloader.Instaloader()

# Read usernames from file
with open('private_users.txt', 'r') as f:
    usernames = f.read().split(',')
usernames = [u.strip() for u in usernames]

# Write header row to CSV file
fieldnames = ['Username', 'Profile Pic', 'Nums/Length Username', 'Full Name Words', 'Bio Length', 'External Url', 'Private', 'Verified', 'Business', '#Posts', '#Followers', '#Following', 'Fake']
with open('private_data.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

# Loop through usernames and extract data
for username in usernames:
    try:
        # Retrieve the profile metadata
        profile = instaloader.Profile.from_username(L.context, username)

        # Extract required details from the profile object
        profile_pic = 0 if "44884218_345707102882519_2446069589734326272_n.jpg" in profile.profile_pic_url else 1
        username = profile.username
        num_username_chars = len(username)
        num_username_nums = sum(c.isdigit() for c in username)
        full_name = profile.full_name
        num_full_name_words = len(full_name.split())
        bio_length = len(profile.biography)
        external_url = 0 if profile.external_url == None else 1
        is_private = 1 if profile.is_private else 0
        is_verified = 1 if profile.is_verified else 0
        is_business_account = 1 if profile.is_business_account else 0
        num_posts = profile.mediacount
        num_followers = profile.followers
        num_following = profile.followees
        fake = 0
        nums_per_uname=round((num_username_nums/num_username_chars),3)

        # Write details to CSV file
        with open('private_data.csv', 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({
                'Username': username,
                'Profile Pic': profile_pic,
                'Nums/Length Username': nums_per_uname,
                'Full Name Words': num_full_name_words,
                'Bio Length': bio_length,
                'External Url': external_url,
                'Private': is_private,
                'Verified': is_verified,
                'Business': is_business_account,
                '#Posts': num_posts,
                '#Followers': num_followers,
                '#Following': num_following,
                'Fake': fake
            })

    except Exception as e:
        print(f"Error processing {username}: {str(e)}")
