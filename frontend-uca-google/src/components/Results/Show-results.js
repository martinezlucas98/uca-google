
import Results from './Results';
//import datos from './datos.json';
import styles from './Results.module.css';
import {useState} from 'react';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';


const ITEMS_PER_PAGE = 2;
function Show_results(props){

  const[datosFromApi, setDatosFromApi] = useState(props.datox.results)
  const[items, setItems] = useState([...props.datox.results].splice(0,ITEMS_PER_PAGE))
  const[currentPage, setCurrentPage] = useState(0)
 
  const nextHandler = () => {
    const totalElementos = datosFromApi.length;
    console.log(totalElementos)
    const nextPage = currentPage + 1;
    console.log(nextPage)
    const firstIndex = nextPage * ITEMS_PER_PAGE;
    console.log(firstIndex)
    if(firstIndex >= totalElementos) return; //Cuando ya no tengo elementos que mostrar
    setItems([...props.datox.results].splice(firstIndex,ITEMS_PER_PAGE))
    setCurrentPage(nextPage)

  }
   //Funcion que se encarga cuando se presione el boton para la pagina anterior
  const prevHandler = () => {
    const prevPage = currentPage - 1
    if(prevPage<0) return; //Cuando estemos en la pagina 0, no podemos ir hacia atras
    const firstIndex = prevPage * ITEMS_PER_PAGE;
    setItems([...props.datox.results].splice(firstIndex,ITEMS_PER_PAGE))

    setCurrentPage(prevPage)
 
  }


  return(
    <div>

      <div className={styles.buttons}>
        <button onClick={prevHandler} className={styles.buttonPrev}> <NavigateBeforeIcon/></button>
        <button onClick={nextHandler} className={styles.buttonNext}><NavigateNextIcon/></button>
      </div>
 
    {
      items.map(dato =>{
        return(
          <Results
          title={dato.title}
          link={dato.url}
          description={dato.description}
        />
        )
      })
    }
    
  
    </div>



  );

}

export default Show_results;
