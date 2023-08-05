use anyhow::Result;

use crate::ast::ast_fold::*;
use crate::ast::*;

pub fn un_group(nodes: Vec<Node>) -> Result<Vec<Node>> {
    UnGrouper {}.fold_nodes(nodes)
}

/// Traverses AST and replaces transforms with nested pipelines with the pipeline
struct UnGrouper {}

impl AstFold for UnGrouper {
    fn fold_nodes(&mut self, nodes: Vec<Node>) -> Result<Vec<Node>> {
        let mut res = Vec::new();

        for node in nodes {
            match node.item {
                Item::Transform(Transform::Group { pipeline, .. }) => {
                    let pipeline = pipeline.item.into_pipeline()?;

                    let pipeline = self.fold_nodes(pipeline.functions)?;

                    res.extend(pipeline);
                }
                _ => {
                    res.push(self.fold_node(node)?);
                }
            }
        }
        Ok(res)
    }
}
