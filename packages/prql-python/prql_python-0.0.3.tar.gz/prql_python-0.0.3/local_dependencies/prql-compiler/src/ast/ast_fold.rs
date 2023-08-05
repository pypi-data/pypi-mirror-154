/// A trait to "fold" a PRQL AST (similiar to a visitor), so we can transitively
/// apply some logic to a whole tree by just defining how we want to handle each
/// type.
use super::*;
use anyhow::Result;
use itertools::Itertools;

// Fold pattern:
// - https://rust-unofficial.github.io/patterns/patterns/creational/fold.html
// Good discussions on the visitor / fold pattern:
// - https://github.com/rust-unofficial/patterns/discussions/236 (within this,
//   this comment looked interesting: https://github.com/rust-unofficial/patterns/discussions/236#discussioncomment-393517)
// - https://news.ycombinator.com/item?id=25620110

// TODO: some of these impls will be too specific because they were copied from
// when ReplaceVariables was implemented directly. When we find a case that is
// overfit on ReplaceVariables, we should add the custom impl to
// ReplaceVariables, and write a more generic impl to this.
pub trait AstFold {
    fn fold_node(&mut self, mut node: Node) -> Result<Node> {
        node.item = self.fold_item(node.item)?;
        Ok(node)
    }
    fn fold_item(&mut self, item: Item) -> Result<Item> {
        fold_item(self, item)
    }
    fn fold_nodes(&mut self, nodes: Vec<Node>) -> Result<Vec<Node>> {
        nodes.into_iter().map(|node| self.fold_node(node)).collect()
    }
    fn fold_ident(&mut self, ident: Ident) -> Result<Ident> {
        Ok(ident)
    }
    fn fold_table(&mut self, table: Table) -> Result<Table> {
        Ok(Table {
            name: self.fold_ident(table.name)?,
            pipeline: Box::new(self.fold_node(*table.pipeline)?),
        })
    }
    // For some functions, we want to call a default impl, because copying &
    // pasting everything apart from a specific match is lots of repetition. So
    // we define a function outside the trait, by default call it, and let
    // implementors override the default while calling the function directly for
    // some cases. Feel free to extend the functions that are separate when
    // necessary. Ref https://stackoverflow.com/a/66077767/3064736
    fn fold_transform(&mut self, transform: Transform) -> Result<Transform> {
        fold_transform(self, transform)
    }
    fn fold_pipeline(&mut self, pipeline: Pipeline) -> Result<Pipeline> {
        fold_pipeline(self, pipeline)
    }
    fn fold_func_def(&mut self, function: FuncDef) -> Result<FuncDef> {
        fold_func_def(self, function)
    }
    fn fold_func_call(&mut self, func_call: FuncCall) -> Result<FuncCall> {
        fold_func_call(self, func_call)
    }
    fn fold_table_ref(&mut self, table_ref: TableRef) -> Result<TableRef> {
        fold_table_ref(self, table_ref)
    }
    fn fold_named_expr(&mut self, named_expr: NamedExpr) -> Result<NamedExpr> {
        fold_named_expr(self, named_expr)
    }
    fn fold_interpolate_item(&mut self, sstring_item: InterpolateItem) -> Result<InterpolateItem> {
        fold_interpolate_item(self, sstring_item)
    }
    fn fold_column_sort(&mut self, column_sort: ColumnSort) -> Result<ColumnSort> {
        fold_column_sort(self, column_sort)
    }
    fn fold_column_sorts(&mut self, columns: Vec<ColumnSort>) -> Result<Vec<ColumnSort>> {
        columns
            .into_iter()
            .map(|c| self.fold_column_sort(c))
            .try_collect()
    }
    fn fold_select(&mut self, select: Select) -> Result<Select> {
        fold_select(self, select)
    }
    fn fold_join_filter(&mut self, f: JoinFilter) -> Result<JoinFilter> {
        fold_join_filter(self, f)
    }
}

pub fn fold_item<T: ?Sized + AstFold>(fold: &mut T, item: Item) -> Result<Item> {
    Ok(match item {
        Item::Ident(ident) => Item::Ident(fold.fold_ident(ident)?),
        Item::Expr(items) => Item::Expr(fold.fold_nodes(items)?),
        Item::List(items) => Item::List(
            items
                .into_iter()
                .map(|x| fold.fold_node(x.into_inner()).map(ListItem))
                .try_collect()?,
        ),
        Item::Range(Range { start, end }) => Item::Range(Range {
            start: fold_optional_box(fold, start)?,
            end: fold_optional_box(fold, end)?,
        }),
        Item::Query(query) => Item::Query(Query {
            nodes: fold.fold_nodes(query.nodes)?,
            ..query
        }),
        Item::Pipeline(p) => Item::Pipeline(fold.fold_pipeline(p)?),
        Item::NamedExpr(named_expr) => Item::NamedExpr(fold.fold_named_expr(named_expr)?),
        Item::Transform(transformation) => Item::Transform(fold.fold_transform(transformation)?),
        Item::SString(items) => Item::SString(
            items
                .into_iter()
                .map(|x| fold.fold_interpolate_item(x))
                .try_collect()?,
        ),
        Item::FString(items) => Item::FString(
            items
                .into_iter()
                .map(|x| fold.fold_interpolate_item(x))
                .try_collect()?,
        ),
        Item::FuncDef(func) => Item::FuncDef(fold.fold_func_def(func)?),
        Item::FuncCall(func_call) => Item::FuncCall(fold.fold_func_call(func_call)?),
        Item::Table(table) => Item::Table(fold.fold_table(table)?),
        // None of these capture variables, so we don't need to replace
        // them.
        Item::String(_) | Item::Raw(_) | Item::Interval(_) => item,
    })
}

pub fn fold_pipeline<T: ?Sized + AstFold>(fold: &mut T, pipeline: Pipeline) -> Result<Pipeline> {
    Ok(Pipeline {
        value: fold_optional_box(fold, pipeline.value)?,
        functions: fold.fold_nodes(pipeline.functions)?,
    })
}

// This aren't strictly in the hierarchy, so we don't need to
// have an assoc. function for `fold_optional_box` — we just
// call out to the function in this module
pub fn fold_optional_box<T: ?Sized + AstFold>(
    fold: &mut T,
    opt: Option<Box<Node>>,
) -> Result<Option<Box<Node>>> {
    Ok(opt.map(|n| fold.fold_node(*n)).transpose()?.map(Box::from))
}

pub fn fold_interpolate_item<T: ?Sized + AstFold>(
    fold: &mut T,
    interpolate_item: InterpolateItem,
) -> Result<InterpolateItem> {
    Ok(match interpolate_item {
        InterpolateItem::String(string) => InterpolateItem::String(string),
        InterpolateItem::Expr(expr) => InterpolateItem::Expr(Box::new(fold.fold_node(*expr)?)),
    })
}

pub fn fold_column_sort<T: ?Sized + AstFold>(
    fold: &mut T,
    sort_column: ColumnSort,
) -> Result<ColumnSort> {
    Ok(ColumnSort {
        direction: sort_column.direction,
        column: fold.fold_node(sort_column.column)?,
    })
}

pub fn fold_transform<T: ?Sized + AstFold>(
    fold: &mut T,
    transformation: Transform,
) -> Result<Transform> {
    match transformation {
        Transform::From(table) => Ok(Transform::From(fold.fold_table_ref(table)?)),

        Transform::Derive(select) => Ok(Transform::Derive(fold.fold_select(select)?)),
        Transform::Select(select) => Ok(Transform::Select(fold.fold_select(select)?)),
        Transform::Aggregate(select) => Ok(Transform::Aggregate(fold.fold_select(select)?)),

        Transform::Filter(items) => Ok(Transform::Filter(fold.fold_nodes(items)?)),
        Transform::Sort(items) => Ok(Transform::Sort(fold.fold_column_sorts(items)?)),
        Transform::Join { side, with, filter } => Ok(Transform::Join {
            side,
            with: fold.fold_table_ref(with)?,
            filter: fold.fold_join_filter(filter)?,
        }),
        Transform::Group { by, pipeline } => Ok(Transform::Group {
            by: fold.fold_nodes(by)?,
            pipeline: Box::new(fold.fold_node(*pipeline)?),
        }),
        // TODO: generalize? Or this never changes?
        Transform::Take(_) => Ok(transformation),
    }
}

pub fn fold_select<T: ?Sized + AstFold>(fold: &mut T, select: Select) -> Result<Select> {
    Ok(Select {
        assigns: fold.fold_nodes(select.assigns)?,
        group: fold.fold_nodes(select.group)?,
        window: select.window.map(|x| fold.fold_nodes(x)).transpose()?,
        sort: select.sort.map(|x| fold.fold_nodes(x)).transpose()?,
    })
}

pub fn fold_join_filter<T: ?Sized + AstFold>(fold: &mut T, f: JoinFilter) -> Result<JoinFilter> {
    Ok(match f {
        JoinFilter::On(nodes) => JoinFilter::On(fold.fold_nodes(nodes)?),
        JoinFilter::Using(nodes) => JoinFilter::Using(fold.fold_nodes(nodes)?),
    })
}

pub fn fold_func_call<T: ?Sized + AstFold>(fold: &mut T, func_call: FuncCall) -> Result<FuncCall> {
    // alternative way, looks nicer but requires cloning
    // for item in &mut call.args {
    //     *item = fold.fold_node(item.clone())?;
    // }

    // for item in &mut call.named_args.values_mut() {
    //     let item = item.as_mut();
    //     *item = fold.fold_node(item.clone())?;
    // }

    Ok(FuncCall {
        // TODO: generalize? Or this never changes?
        name: func_call.name.to_owned(),
        args: func_call
            .args
            .into_iter()
            .map(|item| fold.fold_node(item))
            .try_collect()?,
        named_args: func_call
            .named_args
            .into_iter()
            .map(|(name, expr)| fold.fold_node(*expr).map(|e| (name, Box::from(e))))
            .try_collect()?,
    })
}

pub fn fold_table_ref<T: ?Sized + AstFold>(fold: &mut T, table: TableRef) -> Result<TableRef> {
    Ok(TableRef {
        name: fold.fold_ident(table.name)?,
        alias: table.alias.map(|a| fold.fold_ident(a)).transpose()?,
    })
}

pub fn fold_func_def<T: ?Sized + AstFold>(fold: &mut T, func_def: FuncDef) -> Result<FuncDef> {
    Ok(FuncDef {
        name: fold.fold_ident(func_def.name)?,
        kind: func_def.kind,
        positional_params: fold.fold_nodes(func_def.positional_params)?,
        named_params: fold.fold_nodes(func_def.named_params)?,
        body: Box::new(fold.fold_node(*func_def.body)?),
    })
}

pub fn fold_named_expr<T: ?Sized + AstFold>(
    fold: &mut T,
    named_expr: NamedExpr,
) -> Result<NamedExpr> {
    Ok(NamedExpr {
        name: fold.fold_ident(named_expr.name)?,
        expr: Box::new(fold.fold_node(*named_expr.expr)?),
    })
}
