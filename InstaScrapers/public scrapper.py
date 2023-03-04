import instaloader
import json
import csv
import datetime

L = instaloader.Instaloader()


# Read usernames from file
with open('public_users.txt', 'r') as f:
    usernames = f.read().split(',')
usernames = [u.strip() for u in usernames]

# Write header row to CSV file
fieldnames = ['Username', 'Profile Pic', 'Nums/Length Username', 'Full Name Words', 'Bio Length', 'External Url', 'Private', 'Verified', 'Business', '#Posts', '#Followers', '#Following', 'Last Post Recent', '%Post Single Day', 'Index of Activity', 'Average of Likes', 'Fake']
with open('public_data.csv', 'w', newline='') as f:
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
        
        # Last post date and time
        post = profile.get_posts()[0]
        post_date = post.date_local
        now = datetime.datetime.now()
        time_since_last_post = now - post_date
        last_post_recent = 1 if time_since_last_post.days < 30 else 0
        
        # Percentage of posts made on the most active day of the week
        post_days = [0,0,0,0,0,0,0]
        for post in profile.get_posts():
            post_days[post.date_local.weekday()] += 1
        max_posts_day = max(post_days)
        post_single_day = round((max_posts_day / num_posts) * 100, 2)
        
        # Index of activity
        last_month_posts = list(profile.get_posts()[:30])
        total_likes = sum([post.likes for post in last_month_posts])
        avg_likes_per_post = total_likes / len(last_month_posts)
        index_of_activity = round((num_posts / len(last_month_posts)) * (avg_likes_per_post / num_followers) * 100, 2)
        
        # Average likes per post
        all_posts = list(profile.get_posts())
        total_likes = sum([post.likes for post in all_posts])
        avg_likes_per_post = total_likes / len(all_posts)
        
        fake = 0
        
        nums_per_uname = round((num_username_nums / num_username_chars), 3)

        # Write details to CSV file
        with open('public_data.csv', 'a', newline='') as f:
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
             'Last Post Recent': last_post_recent,  # Add last post recent data here
             '%Post Single Day': post_single_day,  # Add %post single day data here
             'Index of Activity': index_of_activity,  # Add index of activity data here
             'Average of Likes': avg_likes_per_post,  # Add average of likes data here
             'Fake': fake
        })
    except Exception as e:
        print(f"Error processing {username}: {str(e)}")

