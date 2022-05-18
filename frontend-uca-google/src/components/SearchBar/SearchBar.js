import styles from './SearchBar.module.css';
import  SearchIcon  from '@mui/icons-material/Search';
import { useRouter } from 'next/router';
import React, { useState } from 'react';
import Link from 'next/link';


function SearchBar(){

  //La funcion handleClick() se llamara una vez que el usuario le de al boton buscar de la barra,
  //Esta funcion nos rediccionara a otra ruta /results
  const router = useRouter()
  const handleSubmit=(e)=>{
    //console.log(value)
    e.preventDefault();
    router.push({
     pathname: '/results/' + value,
     query: {q:value}
   })
  }

  //La funcion handleChange() se usa para poder utilizar el input del usuario y usamos un useState para obtener ese valor
  const [value, setvalue] = useState("")
  function handleChange(event){
    setvalue(event.target.value)
  }

  return(
    <form onSubmit={handleSubmit}>
      <div className={styles.wrapper}>
        
          
        
        <input type='text' className={styles.input_text} placeholder='Search!' onChange={handleChange} value={value}></input> 

        <button className={styles.button_search} type='submit'>
          <SearchIcon className={styles.icon}/>
        </button>


      </div>
    </form>

  );
}


export default SearchBar;