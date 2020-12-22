from django.shortcuts import render ,redirect
from django.http import HttpResponse
from .models import Profile  , Country  , State , User , language_list 
from itertools import chain
import json
# Create your views here.


def index(request) : 
    st = Profile.objects.all()
    # use the query 
    # select profile.id, first_name ,  last_name , experience , profile.user_id , current_position , state , country , skills   from profile  , country , state , skill  where profile.country_id = country.id and profile.state_id = state.id and profile.skill_id = skill.id   ;


    asd =  Profile.objects.raw(" select profile.id, first_name ,  last_name , experience , profile.user_id , current_position , state , country , skills   from profile  , country , state , skill  where profile.country_id = country.id and profile.state_id = state.id and profile.skill_id = skill.id  ;")
    for i in asd : 
        i.skill =  json.loads( i.skills )
        print( type (  json.loads( i.skills ) ) )
    #select profile.id, first_name ,  last_name , experience , profile.user_id , current_position , state , country , skills   from profile  , country , state , skill , filter_details  where profile.country_id = country.id and profile.state_id = state.id and profile.skill_id = skill.id and profile.user_id = filter_details.user_id and filter_details.language like "E%";

    return render( request , 'index.html' , {'se' : asd })
def search(request) :
    
    user_id = request.GET.get('user_id')
    #print(user_id)
    user_type =  User.objects.raw(" select id , role_id from user where id = " + user_id + "  ; ")
    
    
    for i in user_type : 
        type_user =  i.role_id 
        #print(i.role_id )   

    #we got the user type 

    list_checks = request.GET.get( 'hourlyrate1') 
    
    required_string = "profile.id, profile.first_name ,  profile.last_name , profile.experience , profile.user_id , profile.current_position , state.state , country.country , skill.skills " 
    tables_used = " profile  , country , state , skill , user ,  filter_details "
    condition_string = "profile.country_id = country.id and profile.state_id = state.id and profile.skill_id = skill.id and profile.user_id = user.id  and  filter_details.user_id = profile.user_id  " 


    #set user type 
    user_type = int( type_user ) 
    user_type = 1 + (user_type )%2  
    user_type  = str(  user_type )

    condition_string = condition_string  + " and user.role_id =  " + user_type + " " 

    #set the hourly rate 
    hourly_query = ""
    add_on = 0  
    if  request.GET.get('hourlyrate1')  :
        if add_on == 1 : 
            hourly_query = hourly_query + " or " 

        add_on = 1  

        hourly_query = hourly_query + " ( filter_details.hourly_rate < 5  )  " 
    
    
    if  request.GET.get('hourlyrate2')  :
        if add_on == 1 : 
            hourly_query = hourly_query + " or " 

        add_on = 1  

        hourly_query = hourly_query + " ( filter_details.hourly_rate  >=  5 and filter_details.hourly_rate  < 10  )  " 
    
    
    if  request.GET.get('hourlyrate3')  :
        if add_on == 1 : 
            hourly_query = hourly_query + " or " 

        add_on = 1  

        hourly_query = hourly_query + " ( filter_details.hourly_rate >= 10 and filter_details.hourly_rate  < 100    )  " 
    
    
    if  request.GET.get('hourlyrate4')  :
        if add_on == 1 : 
            hourly_query = hourly_query + " or " 

        add_on = 1  

        hourly_query = hourly_query + " ( filter_details.hourly_rate >= 100  )  " 
    
    


    if len (hourly_query ) : 
        hourly_query =  " and  ( " + hourly_query + " ) " 
    

#now add the value of the location

    if request.GET.get('location') : 
        condition_string = condition_string + "  and  " + "  filter_details.location = " + " '" + request.GET.get('location') + "' " 


#now add the value of the language

    if request.GET.get('language') : 
        condition_string = condition_string + "  and  " + "  filter_details.language = " + " '" + request.GET.get('language') + "' " 

#now add the value of the talent 


    talent_query = ""
    add_on = 0  
    if  request.GET.get('Beginner')  :
        if add_on == 1 : 
            talent_query = talent_query + " or " 

        add_on = 1  

        talent_query = talent_query + " ( filter_details.talent = 'Beginner' )  " 
    
    if  request.GET.get('Intermediate')  :
        if add_on == 1 : 
            talent_query = talent_query + " or " 

        add_on = 1  

        talent_query = talent_query + " ( filter_details.talent = 'Intermediate' )  " 
    
    if  request.GET.get('Expert')  :
        if add_on == 1 : 
            talent_query = talent_query + " or " 

        add_on = 1  

        talent_query = talent_query + " ( filter_details.talent = 'Expert' )  " 
    
    if  request.GET.get('Super Expert')  :
        if add_on == 1 : 
            talent_query = talent_query + " or " 

        add_on = 1  

        talent_query = talent_query + " ( filter_details.talent = 'Super Expert' )  " 
    
    


    if len (talent_query ) : 
        talent_query =  " and  ( " + talent_query + " ) " 
    


# add the search string 


    search_string = " and (  profile.first_name  REGEXP '" + "^" + request.GET.get('fname') + "' or  profile.last_name REGEXP '^" + request.GET.get('fname') +"' "  +   " or LOWER( skill.skills ) REGEXP LOWER ( '" + request.GET.get('fname') + "' )" + ")" 

# add the skill string 


    if request.GET.get('fname') == '' :
        search_string = ""
    print(condition_string)

    query_string = " select  " + required_string + "  from  "  +  tables_used + " where  "  + condition_string + hourly_query  + talent_query + search_string + " ; "
    print(query_string)
    asd =  Profile.objects.raw( query_string )


    if asd != None : 
        for i in asd : 
            if i.skills == None : 
                i.skill = {}
                continue  
            i.skill =  json.loads( i.skills )
        #print( type (  json.loads( i.skills ) ) )
    #select profile.id, first_name ,  last_name , experience , profile.user_id , current_position , state , country , skills   from profile  , country , state , skill , filter_details  where profile.country_id = country.id and profile.state_id = state.id and profile.skill_id = skill.id and profile.user_id = filter_details.user_id and filter_details.language like "E%";
    




    locations = Country.objects.all()
    language_list_ht =  language_list.objects.all()

    return render( request , 'index.html' , {'se' : asd , 'type' : type_user , 'locations' : locations , 'language_list_ht' : language_list_ht ,'pre' :   hourly_query  + talent_query + search_string    })



def search_segment(request) : 
    user_id = request.GET.get('user_id')
    #print(user_id)
    user_type =  User.objects.raw(" select id , role_id from user where id = " + user_id + "  ; ")
    
    
    for i in user_type : 
        type_user =  i.role_id 
        #print(i.role_id )   
     
    required_string = "profile.id, profile.first_name ,  profile.last_name , profile.experience , profile.user_id , profile.current_position , state.state , country.country , skill.skills " 
    tables_used = " profile  , country , state , skill , user ,  filter_details "
    condition_string = "profile.country_id = country.id and profile.state_id = state.id and profile.skill_id = skill.id and profile.user_id = user.id  and  filter_details.user_id = profile.user_id  " 


    cla = request.GET.get("cla")

    if cla == None : 
        cla = ""
    pre = request.GET.get("current")

    if pre == None : 
        pre = ""
        
    condition_string = condition_string +  pre  + " and skill.skill_description = '" + cla + "'"


    query_string = " select  " + required_string + "  from  "  +  tables_used + " where  "  + condition_string + " ; "
    print(query_string)
    asd =  Profile.objects.raw( query_string )


    if asd != None : 
        for i in asd : 
            if i.skills == None : 
                i.skill = {}
                continue  
            i.skill =  json.loads( i.skills )
        #print( type (  json.loads( i.skills ) ) )
    #select profile.id, first_name ,  last_name , experience , profile.user_id , current_position , state , country , skills   from profile  , country , state , skill , filter_details  where profile.country_id = country.id and profile.state_id = state.id and profile.skill_id = skill.id and profile.user_id = filter_details.user_id and filter_details.language like "E%";
    




    locations = Country.objects.all()
    language_list_ht =  language_list.objects.all()

    return render( request , 'index.html' , {'se' : asd , 'type' : type_user , 'locations' : locations , 'language_list_ht' : language_list_ht  , 'pre' : pre })





def message(request) : 
    return render(request , 'message.html')