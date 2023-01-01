# Microsoft Teams

***Microsoft Teams plug-in use to Get Users List, Get Chat Members List, 
Chat Send Message, Get Channel Members List, and Channel Send Message.***


## Word Editor
| Item          |            Value             |
|---------------|:----------------------------:|
| Icon          | ![Microsoft Teams](icon.png) |
| Display Name  |     **Microsoft Teams**      |

### Arun Kumar (arunk@argos-labs.com)

Arun Kumar
* [email](mailto:arunk@argos-labs.com) 
 
## Version Control 
* [4.823.932](setup.yaml)
* Release Date: `August 23, 2022`


## Create credentials from Azure Active Directory

1. Sign in in here: https://azure.microsoft.com/en-in/services/active-directory/

![img.png](img.png)

2. Select Manage Azure Active Directory

![img_1.png](img_1.png)

3. Select App registrations

![img_2.png](img_2.png)

4. Add New registration

![img_3.png](img_3.png)

5. Register app with skype and web rediret url

![img_4.png](img_4.png)

6. Select api permissions

![img_5.png](img_5.png)

7. Add api permissions

![img_6.png](img_6.png)

8. Select Microsoft Graph

![img_7.png](img_7.png)

9. Select  permissions

![img_8.png](img_8.png)

10. Search and check all requied permission names from table and Add permission

![img_9.png](img_9.png)


| permission name             |                   permission desc                   |
|-----------------------------|:---------------------------------------------------:|
| ChannelMember.Read.All      |            Read the members of channels             |
| ChannelMember.ReadWrite.All |        Add and remove members from channels         |
| ChannelMessage.Send         |               	Send channel messages                |
| Chat.ReadWrite              |          Read and write user chat messages          |
| ChatMessage.Send            |               Send user chat messages               |
| Group.ReadWrite.All         |              Read and write all groups              |
| offline_access              | Maintain access to data you have given it access to |
| openid                      |                    Sign users in                    |
| profile                     |              View users' basic profile              |
| User.Read                   |            Sign in and read user profile            |
| User.Read.All               |            Read all users' full profiles            |
| User.ReadBasic.All          |           Read all users' basic profiles            |


11. Select Grant admin consent

![img_10.png](img_10.png)

12. Generate secret token Select certificate & secrets

![img_11.png](img_11.png)

13. Add new secret

![img_12.png](img_12.png)

14. Value Column will be secret token

![img_13.png](img_13.png)

15. Update Manifest "signInAudience": "AzureADMultipleOrgs"

![img_14.png](img_14.png)

## Input (Required)

| OP Type                  | Parameters          | Output                                                |
|--------------------------|---------------------|-------------------------------------------------------|
| Get Users List           |                     | id,displayName,jobTitle,officeLocation,businessPhones |
| Get Chat Members List    | Chat Id             | id,displayName,email                                  |
| Chat Send Message        | Chat Id, Message    | message_id                                            |
| Get Channel Members List | Channel Link        | id,displayName,jobTitle,officeLocation,businessPhones |
| Get Channel Members List | Team Id, Channel Id | id,displayName,jobTitle,officeLocation,businessPhones |
| Channel Send Message     | Channel Link        | message_id                                            |
|                          | Message             |                                                       |
| Channel Send Message     | Channel Link        | message_id                                            |
|                          | Message             |                                                       |
|                          | File                |                                                       |
| Channel Send Message     | Team Id, Channel Id | Updated file path                                     |
|                          | Message             |                                                       |
| Channel Send Message     | Team Id, Channel Id | Updated file path                                     |
|                          | Message             |                                                       |
|                          | File                |                                                       |



## Return Value

### Normal Case

Description of the output result

## Return Code
| Code | Meaning                      |
|------|------------------------------|
| 0    | Success                      |
| 1    | Exceptional case             |

## Output Format
You may choose one of 3 output formats below,

<ul>
  <li>String (default)</li>
  <li>CSV</li>
  <li>File</li>
</ul>  


## Parameter setting examples (diagrams)

## Operations

### Get Users List:

![Microsoft Teams Input Data](README_1.png)

### Get Chat Members List:

![Microsoft Teams Input Data](README_2.png)

### Chat Send Message:

![Microsoft Teams Input Data](README_3.png)

### Get Channel Members List:

![Microsoft Teams Input Data](README_4.png)

### Channel Send Message:

![Microsoft Teams Input Data](README_5.png)