
Effective learning vs overfitting
![[Genome#^69e9fa]]
- Comparable to machine learning: mixture of bias (remembering) & generalization (forgetting)


机器学习让我意识到，bias 只有在信息不足的时候才是 bias

任何结果由什么过程导致，这个数量永远可以增加
因素的数量越多就越精确
这个在模型很粗糙的时候叫 generalization，但逐渐更加精细就是 variation 了

正如 sapolsky 所举例的三个仙人掌，一个基因在不同气候下对它们高度的排序完全相反，正说明“控制变量”的这些被控制的变量，是带有巨大 interaction（depends）信息和条件的

那么一个有效的模型，在越精细后、越能够模拟真实反映后，对人来说就越难以用几个恒定的关系/系数/比例/趋势来衡量，因为它们每一个都建立在彼此微小变化的基础上，构成一个非常复杂、易变的网络，共同影响最终的结果

反之为了让人能够理解，我们就不得不对模型进行简化，对不必要的细节抹去，留下一些诚实说是偏见，但也比过度繁杂的信息更有实际用处的规律