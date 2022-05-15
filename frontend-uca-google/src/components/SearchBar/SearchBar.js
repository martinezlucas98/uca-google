import styles from './SearchBar.module.css';
import  SearchIcon  from '@mui/icons-material/Search';
import { useRouter } from 'next/router';


function SearchBar(){

  const router = useRouter()
  const handleClick=()=>{
    router.push('../results')
  }
  
  return(
    <div className={styles.wrapper}>
      
      <input className={styles.input_text} placeholder='Search!'></input> 

      <button className={styles.button_search} onClick={handleClick}>
        <SearchIcon className={styles.icon}/>
      </button>


    </div>

  );
}


export default SearchBar;