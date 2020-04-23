from wrestlr.transformers import TransformExpr
from wrestlr import ast 

code = '''                        
        a <- mtcars %>%                             
          filter(cyl == 6) %>%                 
          mutate(avg_hp = mean(hp))            
        '''                                    


tree = ast.rlang.parse(code, "prog")           
tree2 = TransformExpr().visit(tree)
