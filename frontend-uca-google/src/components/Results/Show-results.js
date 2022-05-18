
import Results from './Results';
//import datos from './datos.json';
import styles from './Results.module.css';

function Show_results(props){
  return(
    <div>
    {
      props.datox.map(dato =>{
        return(
          <Results
          key={dato.id}
          link={dato.website}
          description={dato.name}
        />
        )
      })
    }

    </div>

  );

}

export default Show_results;
