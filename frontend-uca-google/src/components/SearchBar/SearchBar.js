import styles from './SearchBar.module.css';
import  SearchIcon  from '@mui/icons-material/Search';
import { useRouter } from 'next/router';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';

import Autocomplete from './Autocomplete/Autocomplete.js'


function SearchBar(){

  //La funcion handleClick() se llamara una vez que el usuario le de al boton buscar de la barra,
  //Esta funcion nos rediccionara a otra ruta /results
  const [autocompletOpts, setAutocompleteOpts] = useState([]);

  const [focused, setFocused] = useState(false)

  const onFocus = () => setFocused(true)
  const onBlur = () => setFocused(false)

  let [showAutoComplete, setShowAutoComplete] = useState(false);
  
  
  const router = useRouter()
  const handleSubmit=(e)=>{
    //console.log(value)
    e.preventDefault();
    //Verificamos que lo que escribio el usuario no sea vacio
    if(value.length != 0){
      router.push({
        pathname: '/loading/results',
        query: {q:value}
      })
    }
    setvalue("")
    
  }

  
  const [value, setvalue] = useState("")

 
  useEffect(()=>{
    const fetchAutocomplete = async () => {
      const response =  await fetch('http://127.0.0.1:8081/autocomplete?q='+ value, {
        method: 'GET',
       
      })
      .catch((error) =>{
        
        setAutocompleteOpts([]); // si no anda el servidor o que retorna lista vacia
      });

      try {
        if (await response.status != 200){
          setAutocompleteOpts([]);
        }
        let data = await response.json();
        console.log(data['autocompletes'])
        setAutocompleteOpts(data['autocompletes']);
      }
      catch (e) {
        console.log("error en autocomplete");
      }
      
      

        
    }

    fetchAutocomplete();
     

      
    
  },[value]) ;
 
  //La funcion handleChange() se usa para poder utilizar el input del usuario y usamos un useState para obtener ese valor
  function handleChange(event){
    setvalue(event.target.value)
  }

  return(
    <form onSubmit={handleSubmit} >
      <div id = "search" className={styles.wrapper}>
        <input onClick={()=>{setShowAutoComplete(true)}} type='text' className={styles.input_text} placeholder='Search!' onChange={handleChange} value={value} ></input> 
        <button className={styles.button_search} type='submit'>
          <SearchIcon  className={styles.icon}/>
        </button>
      </div>
      <Autocomplete arr={autocompletOpts} setSelectedOpt={setvalue} show={showAutoComplete} onClickOutside={()=> {setShowAutoComplete(false)}}/>
      
     
    </form>
  
    

  );
}


export default SearchBar;