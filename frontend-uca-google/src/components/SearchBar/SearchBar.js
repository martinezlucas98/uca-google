import styles from './SearchBar.module.css';
import  SearchIcon  from '@mui/icons-material/Search';


function SearchBar(){
  return(
    <div className={styles.wrapper}>
      
      <input className={styles.input_text} placeholder='Search!'></input> 

      <button className={styles.button_search}>
        <SearchIcon className={styles.icon}/>
      </button>


    </div>

  );
}


export default SearchBar;