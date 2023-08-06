use pyo3::prelude::*;

use std::fs::File;
use std::io::{Write, Error, BufReader};
use crepe::crepe;
use std::fmt;
use serde::Deserialize;

const IS_A: &str = "rdfs:subClassOf";
const SUB_PROPERTY_OF: &str = "rdfs:subPropertyOf";
const TYPE: &str = "rdf:type";
const TRANSITIVE_PROPERTY: &str = "owl:TransitiveProperty";

crepe! {
    @input
    struct Edge(&'static str, &'static str, &'static str);
    struct Transitive(&'static str);

    @output
    struct EntailedEdge(&'static str, &'static str, &'static str);

    EntailedEdge(x, p, y) <- Edge(x, p, y);
    EntailedEdge(x, p, y) <- EntailedEdge(x, q, y), EntailedEdge(q, SUB_PROPERTY_OF, p);
    EntailedEdge(x, p, z) <- EntailedEdge(x, p, y), EntailedEdge(y, p, z), Transitive(p);
    EntailedEdge(x, p, z) <- EntailedEdge(x, p, y), EntailedEdge(y, IS_A, z);
    EntailedEdge(x, p, z) <- EntailedEdge(x, IS_A, y), EntailedEdge(y, p, z);
    Transitive(IS_A);
    Transitive(SUB_PROPERTY_OF);
    Transitive(p) <- Edge(p, TYPE, TRANSITIVE_PROPERTY);
}

//#[derive(Debug)]
#[derive(Deserialize)]
struct Triple{
    subject: String,
    predicate: String,
    object: String,
}
struct Database<'a> {
    triples: &'a mut Vec<Triple>
}

impl fmt::Display for Triple {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
      write!(f, "{} {} {}", self.subject, self.predicate, self.object)
    }
}

fn parse(database: &mut Database, path: String) -> Result<(), Error> {
    let input = File::open(path)?;
    let reader = BufReader::new(input);
    let mut rdr = csv::Reader::from_reader(reader);
    for triple in rdr.deserialize() {
        let triple: Triple = triple?;
        //println!("{}", triple);
        database.triples.push(triple);
        //println!("{}", database.triples.len());
    }
    Ok(())
}

fn reason(triples: &'static Vec<Triple>, output_path: String) -> Result<(), Error> {
    let mut output = File::create(output_path)?;
    let mut runtime = Crepe::new();
    //runtime.extend(&[Edge("1", IS_A, "2"), Edge("2", "is_a", "3"), Edge("3", "is_a", "4"), Edge("2", "is_a", "5")]);
    for t in triples {
        //println!("{}", t);
        runtime.extend(&[Edge(&t.subject, &t.predicate, &t.object)]);
    }
    let (entailed_edges,) = runtime.run();
    for EntailedEdge(x, p, y) in entailed_edges {
        writeln!(output, "{},{},{}", x, p, y)?;
    }
    Ok(())
}


#[pyfunction]
fn run_relation_graph(path: String, output_path: String) -> PyResult<()> {

    unsafe {
        static mut TRIPLES: Vec<Triple> = Vec::new();
        let mut db: Database = Database{triples: &mut TRIPLES};
        if let Ok(_v) = parse(&mut db, path) {
            if let Ok(_)  = reason(&TRIPLES, output_path) {
                ()
            }
        }
    }
    Ok(())
}

/// A Python module implemented in Rust.
#[pymodule]
fn relation_graph_impl(_py: Python, m: &PyModule) -> PyResult<()> {
    //m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(run_relation_graph, m)?)?;
    Ok(())
}